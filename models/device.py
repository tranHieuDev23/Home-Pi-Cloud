import enum


class DeviceType(enum):
    SMART_LIGHT = 'SMART_LIGHT'
    THERMOSTAT = 'THERMOSTAT'


class Device:
    def __init__(self, id, display_name, type, owner, status) -> None:
        self.id = id
        self.display_name = display_name
        self.type = type
        self.owner = owner
        self.status = status
