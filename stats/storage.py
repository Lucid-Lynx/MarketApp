import logging
from datetime import date

logging.basicConfig(level=logging.INFO)


class Storage:

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Storage, cls).__new__(cls)
        return cls.instance

    def __init__(self, values=None):
        if not len(self.__dict__):
            self.values = values if values else []

    def add_value(self, value, current_date=date.today().toordinal()):
        self.values.append({
            'date': current_date,
            'value': value,
        })

    def clean(self):
        self.values.clear()
