#
#  Copyright (c) 2018-2019 Renesas Inc.
#  Copyright (c) 2018-2019 EPAM Systems Inc.
#

import hashlib
import logging
import time
from abc import ABCMeta, abstractmethod

from aos_provisioning.onboard.config import Config
from aos_provisioning.utils.errors import BoardError
from aos_provisioning.utils.security import PubKeys

logger = logging.getLogger(__name__)


class BoardBase(object):
    __metaclass__ = ABCMeta

    PATH_MODEL_NAME = '/var/aos/model_name.txt'

    def __init__(self):
        self._connector = None
        self._config = Config()

    @abstractmethod
    def init_connector(self):
        pass

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()

    def connect(self):
        self._connector = self.init_connector()

    def disconnect(self):
        if self._connector:
            self._connector.close()
            self._connector = None

    def is_file_exist(self, filename):
        ret = self.connector.execute("test -e {}".format(filename))
        return not ret.exit_code

    def get_file_size(self, filename):
        ret = self.connector.execute("stat -c %s {}".format(filename))
        if not ret.exit_code:
            return int(ret.data)

    def cat_file(self, filename, file_len, allow_empty=False):
        while True:
            try:
                ret = self.connector.execute("cat {}".format(filename))
                if ret.exit_code:
                    logger.error('Failed to get {} from the board'.format(filename))
                    raise AssertionError
                result = ret.data

                if len(result) != file_len and len(result) + 1 != file_len:
                    logger.debug("Received data size is (%s), expected (%s)", str(len(result)), str(file_len))
                    if not len(result) and allow_empty:
                        return ""
                    time.sleep(0.5)
                else:
                    if isinstance(result, bytes):
                        result = result.decode()
                    return result
            except ValueError:
                pass

    def read_file(self, filename):
        if not self.is_file_exist(filename):
            return None

        file_size = self.get_file_size(filename)
        if file_size == 0:
            return ''

        return self.cat_file(filename, file_size)

    def create_dir(self, dir_path):
        cmd = "mkdir -p {}".format(dir_path)
        resp = self.connector.execute(cmd)
        if resp.exit_code:
            logger.error("Failed to create dir %s", dir_path)
            raise BoardError("Failed to create dir %s", dir_path)

    def delete_dir(self, dir_path, check_for_presence=False):
        if check_for_presence and not self.is_file_exist(dir_path):
            logger.debug('Dir %s not exist. Skipping delete.', dir_path)
            return

        cmd = "rm -r {}".format(dir_path)
        resp = self.connector.execute(cmd)
        if resp.exit_code:
            logger.error("Failed to delete dir or file %s", dir_path)
            raise BoardError("Failed to delete dir or file %s", dir_path)
        else:
            logger.debug("Deleted: %s", dir_path)

    def write_to_file(self, filename, content, retry_count=5):
        cmd = "echo '{}' > {}".format(content, filename)
        try:
            logger.info("Uploading file {}.".format(filename))
            retry_count -= 1
            self.connector.execute(cmd, debug=False)
            while retry_count > 0 and not self._validate_content_upload(content, filename, True):
                logger.info("Upload file {} failed. Retry count left {}".format(filename, retry_count))
                self.connector.execute(cmd, debug=False)
                retry_count -= 1
        except ValueError:
            pass

    def _read_checksum(self, filename):
        """ Calculate file checksum on board. """
        ret = self.connector.execute("sha1sum {}".format(filename))
        logger.debug('sha1 ' + str(ret))
        if ret.exit_code:
            return False

        if isinstance(ret.data, bytes):
            ret.data = ret.data.decode()
        logger.debug("received checksum: [" + str(ret.data) + "]")
        splitted = list(filter(None, ret.data.split(" ")))
        logger.debug('splitted: ' + str(splitted))
        if len(splitted) == 2 and splitted[1].strip('\n') == filename:
            logger.debug("received checksum: {}".format(splitted[0]))
            return splitted[0]

        return False

    def _validate_content_upload(self, content, target_file_name, add_new_line=False):
        target_checksum = self._read_checksum(target_file_name)
        logger.debug("UPl check " + str(target_checksum))
        if not target_checksum:
            return False

        m = hashlib.sha1()
        m.update(content.encode('utf-8'))
        if add_new_line:
            m.update('\n'.encode('utf-8'))

        logger.debug("Content digest is {}, Board file digest is {}".format(m.hexdigest(), target_checksum))
        logger.debug("File digetst = %s", m.hexdigest())
        logger.debug("Target digetst = %s", target_checksum)
        logger.debug("File = %s", content)
        return m.hexdigest() == target_checksum

    def _set_slashes_to_paths_end(self):
        if not self.config.online_key_folder.endswith("/"):
            self.config.online_key_folder = self.config.online_key_folder + '/'

        if not self.config.online_cert_folder.endswith("/"):
            self.config.online_cert_folder = self.config.online_cert_folder + '/'

        if not self.config.offline_key_folder.endswith("/"):
            self.config.offline_key_folder = self.config.offline_key_folder + '/'

        if not self.config.offline_cert_folder.endswith("/"):
            self.config.offline_cert_folder = self.config.offline_cert_folder + '/'

    @property
    def connector(self):
        return self._connector

    @property
    def config(self):
        return self._config

    @abstractmethod
    def _generate_pair(self, pair_type):
        pass

    @abstractmethod
    def get_hw_id(self):
        pass

    @abstractmethod
    def get_system_id(self):
        pass

    @abstractmethod
    def get_model_name(self):
        pass

    @abstractmethod
    def get_init_data(self):
        pass

    def generate_pkeys(self):
        """ Generates a key pair. Returns object with public ones. """
        logger.info("Generating security keys ...")

        pkeys = PubKeys()
        for t in PubKeys.TYPES:
            logger.debug("Generating %s key pairs ...", t)

            public = self._generate_pair(t)

            if t == PubKeys.TYPE_ONLINE:
                pkeys.online = public
            elif t == PubKeys.TYPE_OFFLINE:
                pkeys.offline = public

        self._config.set_keys(pkeys)
        return pkeys

    @abstractmethod
    def configure(self):
        pass

    @abstractmethod
    def perform_deprovisioning(self):
        pass
