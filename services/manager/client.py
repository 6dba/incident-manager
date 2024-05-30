"""
Клиенты для подключения к файловым сетевым ресурсам
"""
__author__ = "6dba"
__date__ = "18/05/2024"

import os
import ftplib
from smb.SMBConnection import SMBConnection

from core.settings import settings


class SMBClient:
    """
    SMB клиент
    """
    def __init__(self):
        self.__name = settings.SMB_SHARE_NAME
        self.__host = settings.SMB_HOST
        self.__dir = settings.SMB_SHARE_DIR_PATH
        self.__username = settings.SMB_USERNAME
        self.__password = settings.SMB_PASSWORD

    def upload(self, local_file_path, target_file_path):
        """
        Загрузка файла на SMB сервер

        :param local_file_path:
        :param target_file_path:
        :return:
        """
        if not self.__host:
            return

        connection = SMBConnection(
            self.__username, self.__password, 'incident-manager-file-service', self.__name, use_ntlm_v2=True
        )
        connection.connect(self.__host)
        with open(local_file_path, 'rb') as file:
            connection.storeFile(self.__dir, target_file_path, file, os.path.getsize(local_file_path))
        connection.close()


class FTPClient:
    """
    FTP клиент
    """
    def __init__(self):
        self.__host = settings.FTP_HOST
        self.__user = settings.FTP_USER
        self.__password = settings.FTP_PASSWORD
        self.__target_dir = settings.FTP_DIR_PATH

    def upload(self, local_file_path, target_file_name):
        """
        Загрузка файла на FTP сервер

        :param local_file_path:
        :param target_file_name:
        :return:
        """
        if not self.__host:
            return

        # Отправка файла по FTP
        with ftplib.FTP(self.__host, self.__user or 'anonymous', self.__password or '') as ftp, \
                open(local_file_path, 'rb') as file:
            if self.__target_dir:
                ftp.cwd(self.__target_dir)
            # Переключаемся в бинарный режим передачи данных
            ftp.set_pasv(True)
            ftp.storbinary(f'STOR {target_file_name}', file)
