import random as rn

class DateFinder:
    def __init__(self) -> None:
        self.days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Firday", "Saturday"]

        self.norm_doomse_days = ["04/04", "06/06", "08/08", "10/10", "12/12", "09/05", "05/09", "11/07", "07/11", "14/03"]
        self.rel_months = [date[3:5] for date in self.norm_doomse_days]

        self.changing_doomse_days = {
            "not_leap": ["03/01", "28/02"],
            "leap": ["04/01", "29/02"]
        }

        self.dooms_day_2000 = 2
    
    def is_leap(self, year: int):
        return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)
    
    def years_and_leap_years_since_2000(self, year: int):
        years_bw = abs(year - 2000)

        leaps_bw = int(years_bw / 4) - int(years_bw / 100) + int(years_bw / 400)
        
        if year < 2000:
            years_bw = -years_bw
            leaps_bw = -leaps_bw
            leaps_bw -= 1
        
        return years_bw, leaps_bw

    def calculate_doomsday_date(self, year: str):
        years_since_2000, leaps_since_2000 = self.years_and_leap_years_since_2000(int(year))

        return (self.dooms_day_2000 + years_since_2000 + leaps_since_2000) % 7
    
    def calculate_weekday(self, date: str):

        year = date[6:]
        
        dooms_day_date = self.calculate_doomsday_date(year)

        leap = self.is_leap(int(year))
        day_month = date[0:5]

        # if we were lucky enough to get and actual doomsday
        if day_month in self.norm_doomse_days or (not leap and day_month in self.changing_doomse_days["not_leap"]) or (leap and day_month in self.changing_doomse_days["leap"]):
            return self.days[dooms_day_date]
        
        day = date[0:2]
        month = date[3:5]

        int_month = int(month)

        # handles for feb and jan
        if int_month == 2:
            if leap:
                doomse_day = int(self.changing_doomse_days["leap"][1][0:2])
                diff = int(day) - doomse_day

                return self.days[(dooms_day_date + diff) % 7]
            else:
                doomse_day = int(self.changing_doomse_days["not_leap"][1][0:2])
                diff = int(day) - doomse_day

                return self.days[(dooms_day_date + diff) % 7]
        elif int_month == 1:
            if leap:
                doomse_day = int(self.changing_doomse_days["leap"][0][0:2])
                diff = int(day) - doomse_day

                return self.days[(dooms_day_date + diff) % 7]
            else:
                doomse_day = int(self.changing_doomse_days["not_leap"][0][0:2])
                diff = int(day) - doomse_day

                return self.days[(dooms_day_date + diff) % 7]
        else:
            month_index = self.rel_months.index(month)
            doomse_day = int(self.norm_doomse_days[month_index][0:2])
            diff = int(day) - doomse_day

            return self.days[(dooms_day_date + diff) % 7]

    def calculate_weekday_val(self, date:str):
        
        year = date[6:]
        
        dooms_day_date = self.calculate_doomsday_date(year)

        leap = self.is_leap(int(year))
        day_month = date[0:5]

        # if we were lucky enough to get and actual doomsday
        if day_month in self.norm_doomse_days or (not leap and day_month in self.changing_doomse_days["not_leap"]) or (leap and day_month in self.changing_doomse_days["leap"]):
            return dooms_day_date
        
        day = date[0:2]
        month = date[3:5]

        int_month = int(month)

        # handles for feb and jan
        if int_month == 2:
            if leap:
                doomse_day = int(self.changing_doomse_days["leap"][1][0:2])
                diff = int(day) - doomse_day

                return (dooms_day_date + diff) % 7
            else:
                doomse_day = int(self.changing_doomse_days["not_leap"][1][0:2])
                diff = int(day) - doomse_day

                return (dooms_day_date + diff) % 7
        elif int_month == 1:
            if leap:
                doomse_day = int(self.changing_doomse_days["leap"][0][0:2])
                diff = int(day) - doomse_day

                return (dooms_day_date + diff) % 7
            else:
                doomse_day = int(self.changing_doomse_days["not_leap"][0][0:2])
                diff = int(day) - doomse_day

                return (dooms_day_date + diff) % 7
        else:
            month_index = self.rel_months.index(month)
            doomse_day = int(self.norm_doomse_days[month_index][0:2])
            diff = int(day) - doomse_day

            return (dooms_day_date + diff) % 7
    
    def generate_random_date(self):
        month = rn.randint(1, 12)
        year = rn.randint(1, 6000)
        if month == 2 and self.is_leap(year):
            day_range = 29
        elif month == 2:
            day_range = 28
        elif month == 4 or month == 6 or month == 9 or month == 11:
            day_range = 30
        else:
            day_range = 31
        day = rn.randint(1, day_range)

        year_str = str(year)
        if month < 10:
            month_str = f"0{month}"
        else:
            month_str = str(month)
        if day < 10:
            day_str = f"0{day}"
        else:
            day_str = str(day)
        
        return f"{day_str}/{month_str}/{year_str}"
    
    def generate_random_day(self):
        date = self.generate_random_date()
        day_val = self.calculate_weekday_val(date)
        return {"date": date, "day_val": day_val, "day": self.days[day_val]}

class Ui:
    def __init__(self) -> None:
        self.finder = DateFinder()

        self.err_statment = "Invalid input :(\nTry again."

    def get_date(self):
        date = ""

        while date == "":
            attempt = input("Enter a date or 'q' to quit (hint: 3 July, 1951 should be put as 03/07/1951): ")

            # check if input is q
            if attempt == "q":
                quit()

            #check if len is ok
            if len(attempt) < 7:
                print(self.err_statment)
                continue

            # check if the slashes are in the right places and all inputs are right len
            if attempt[2] != "/" or attempt[5] != "/" or "/" in attempt[0:2] or "/" in attempt[3:5]:
                print(self.err_statment)
                continue
            
            day = attempt[0:2]
            month = attempt[3:5]
            year = attempt[6:]

            # make sure all inputs are ints
            try:
                day_int = int(day)
                month_int = int(month)
                year_int = int(year)
            except Exception as _:
                print(self.err_statment)
                continue
            if day_int != float(day) or month_int != float(month) or year_int != float(year):
                print(self.err_statment)
                continue

            # check that day month and year are all valid
            if day_int < 1 or day_int > 31 or month_int > 12 or month_int < 1 or year_int < 1 or (month_int == 2 and day_int > 29) or (not self.finder.is_leap(year_int) and month_int == 2 and day_int > 28):
                print(self.err_statment)
                continue
            if day_int > 30 and (month_int == 4 or month_int == 6 or month_int == 9 or month_int == 11):
                print(self.err_statment)
                continue
                
            date = attempt
        
        return date
    
    def get_weekday(self):
        date = self.get_date()
        day = self.finder.calculate_weekday(date)
        return f"The weekday of {date} is {day}."

ui = Ui()
# for _ in range(100):
#     print(ui.finder.generate_random_day())
print(ui.get_weekday())
