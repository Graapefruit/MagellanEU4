from datetime import date

class ProvinceUpdate:
    def __init__(self, year, month, day, text):
            self.date = date(year, month, day)
            self.text = text