from os.path import exists, join
from unittest import TestCase

from . import *


class FilesExist(TestCase):
    def test_firebase_secret_exist(self):
        """ checks if firebase.secret is in project level directory """
        self.assertEqual(exists(SETTINGS["FIREBASE_SECRET"]), True)

    def test_database_endpoint_exist(self):
        """ checks if databaseurl.secret is in project level directory """
        self.assertEqual(exists(SETTINGS["DATABASE_ENDPOINT"]), True)


class Headers(TestCase):
    ARDUINO_FILE_PATH = join(ROOT_DIR, join("arduino", "arduino.ino"))

    def test_read_headers_math(self):
        headers = COMM_CODES["READ"]
        file_lines = open(self.ARDUINO_FILE_PATH, "r").read().splitlines()
        for line in file_lines:
            if "const byte " in line:
                for header in headers:
                    if header in line:
                        python_value = headers[header]
                        arduino_value = int(
                            line.split("= ")[1].replace(";", "").split("0x")[1], 16
                        )
                        self.assertEqual(python_value, arduino_value)

    def test_write_headers_math(self):
        headers = COMM_CODES["WRITE"]
        file_lines = open(self.ARDUINO_FILE_PATH, "r").read().splitlines()
        for line in file_lines:
            if "const int " in line:
                for header in headers:
                    if header in line:
                        python_value = ord(headers[header])
                        arduino_value = int(line.split("= ")[1].replace(";", ""))
                        self.assertEqual(python_value, arduino_value)
