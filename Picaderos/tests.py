import time
from datetime import timedelta, datetime

first_date = '2021-01-01'
final_date = '2021-12-31'
first_date = datetime.strptime(first_date, '%Y-%m-%d')
last_date = datetime.strptime(final_date, '%Y-%m-%d')
week_day = 1
dates = [first_date + timedelta(days=x) for x in range((last_date - first_date).days + 1) if (first_date + timedelta(days=x)).weekday() == 1]

print(first_date.strftime('%A'))
