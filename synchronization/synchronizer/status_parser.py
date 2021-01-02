# Created by quangkhanh at 02/01/2021
# File: status_parser.py
from synchronization.data.info import Info
from synchronization.synchronizer.parser import Parser

import re


class StatusParser(Parser):

    def __init__(self):
        self.__pattern = "(.*)/(.*)/(.*)"

    def parse(self, content: str) -> Info:
        result = re.match(self.__pattern, content)
        if result is not None:
            username = result.group(1)
            address = "iot_db.device"
            id = result.group(2)
            status = result.group(3)
            return Info(address, id, status)
        else:
            return None
