from fastapi import FastAPI,Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import datetime
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
        # this is horrible horrible code bc im basicly just walking backwards, but i wrote "calculate_weekday" first
        return self.days.index(self.calculate_weekday(date))
    
    def generate_random_date(self):
        month = rn.randint(1, 12)
        year = rn.randint(1, 6000)
        if month == 2 and self.is_leap(year):
            day_range = 29
        elif month == 2:
            day_range = 28
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
        return date, self.calculate_weekday(date)


app = FastAPI()

templates = Jinja2Templates("./api_templates")

@app.get("/", response_class=HTMLResponse)
def home(req:Request, date:str="2000-01-01"): # y-m-d

    year_index = date.index("-")
    year = date[0:year_index]
    month = date[year_index+1:year_index+3]
    day = date[year_index+4:year_index+6]

    int_year = int(year)
    int_month = int(month)
    int_day = int(day)

    date_str = f"{month}/{day}/{year}"

    finder = DateFinder()

    now = datetime.datetime.now()
    tense = ""

    if int_year > now.year:
        tense = "Will Be"
    elif int_year < now.year:
        tense = "Was"
    else:
        inputed = datetime.datetime(int_year, int_month, int_day, now.hour, now.minute, now.second, now.microsecond)
        if inputed > now:
            tense = "Will Be"
        elif inputed < now:
            tense = "Was"
        else:
            tense = "Is"

    weekday = finder.calculate_weekday(f"{day}/{month}/{year}")

    return templates.TemplateResponse("home.html", {"request": req, "date": date_str, "tense": tense, "weekday": weekday})

@app.get("/test")
def test(num: str=None):
    return {"num": num}

