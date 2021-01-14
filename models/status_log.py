class StatusLog:
    def __init__(self, id, of_device, timestamp, field_name, field_value):
        self.id = id
        self.of_device = of_device
        self.timestamp = timestamp
        self.field_name = field_name
        self.field_value = field_value
