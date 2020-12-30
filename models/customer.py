class Customer:
    def __init__(self, customer_name, password, display_name, devices=None, commanders=None):
        self.customer_name = customer_name
        self.password = password
        self.display_name = display_name
        self.devices = devices
        self.commanders = commanders
