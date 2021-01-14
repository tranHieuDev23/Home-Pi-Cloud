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


def is_supported_command(type: DeviceType, command: str):
    if (type == DeviceType.LIGHT):
        return command in ['turnOn', 'turnOff']
    return False
