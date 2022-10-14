from django.test import TestCase
from datetime import date 
  
def calculateAge(birthDate): 
    today = date.today() 
    age = today.year - birthDate.year -  ((today.month, today.day) < (birthDate.month, birthDate.day)) 
    return age 
      
# print(calculateAge(date(2004, 10, 6)), "years") 



import datetime
TODAY_CHECK = datetime.datetime.now()
start = datetime.datetime.strptime("01-10-2022", "%d-%m-%Y")
end = datetime.datetime.strptime("06-10-2022", "%d-%m-%Y")
if start <= TODAY_CHECK <= end or start == TODAY_CHECK == end :
    print ("PASS!")
else:
    print ("YOU SHALL NOT PASS, FRODO.")


# Create your tests here.
