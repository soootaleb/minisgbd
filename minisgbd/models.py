from helpers import c

class RelSchema:
    name = 'DEFAULT_RELSCHEMA_NAME'
    columns_types = []
    columns_number = 0

    def __init__(self, name, columns_types, columns_number):
        self.name = name
        self.columns_types = columns_types
        self.columns_number = columns_number

    def __str__(self):
        return c(self.name) + ' with columns ' + str(self.columns_types)