class StatusLog:
    def __init__(self, id, ofDevice, timestamp, fieldName, fieldValue):
        self.id = id
        self.ofDevice = ofDevice
        self.timestamp = timestamp
        self.fieldName = fieldName
        self.fieldValue = fieldValue
