class User:
    def __init__(self, username, displayName, password=None, commandTopic=None, statusTopic=None):
        self.username = username
        self.displayName = displayName
        self.password = password
        self.commandTopic = commandTopic
        self.statusTopic = statusTopic
