import calendar
import datetime

days = ['Hétfő', 'Kedd', 'Szerda', 'Csütörtök', 'Péntek', 'Szombat', 'Vasárnap']
months = ['', 'Január', 'Február', 'Március', 'Április', 'Május', 'Június', 'Július',
          'Augusztus', 'Szeptember', 'Október', 'November', 'December']

short_day_names = ['H ', 'K ', 'Sz ', 'Cs ', 'Pt ', 'Szo ', 'V ']


# Hány nap egy hónap
month_days = calendar.mdays
# print(month_days)

# Aktuális dátum és a jelenlegi idő
today_day_name = datetime.datetime.now()
# print(today_day_name)

# Dátum
today_date = datetime.date.today()
# print(today_date)

# Holnapi dátum és a jelenlegi idő
tomorrow_day_name = datetime.datetime.now() + datetime.timedelta(days=1)
# print(tomorrow_day_name)

#Holnapi dátum
tomorrow_date = (datetime.date.today() + datetime.timedelta(days=1))
# print(tomorrow_date)

def one_month(month, year):
    try:
        month = abs(int(month))
        year = abs(int(year))
        week_day_name = calendar.day_abbr
        calendar_months = calendar.monthcalendar(year, month)
        len_calendar_months = len(list(calendar_months))
        month_name = months[month]

        return [calendar_months, len_calendar_months, year, month_name, week_day_name]
    except Exception:
        return False
