from datetime import datetime
import json


days=[]
day = '05-10-2022'
day = datetime.strptime(day, '%d-%m-%Y')
days.append(day.strftime('%A'))
