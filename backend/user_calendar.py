

class UserCalendar:
    
    def __init__(self, name, time_min, time_max, busy_dates):
        self.name = name
        self.time_min = time_min
        self.time_max = time_max
        self.busy_dates = busy_dates

    def __eq__(self, other):
        return self.name == other.name
