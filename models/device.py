from enum import Enum


class DeviceType(Enum):
    LIGHT = 'LIGHT'
    THERMOSTAT = 'THERMOSTAT'


class Device:
    def __init__(self, id, displayName, type, owner):
        self.id = id
        self.displayName = displayName
        self.type = type
        self.owner = owner
