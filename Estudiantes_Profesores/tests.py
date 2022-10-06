from django.test import TestCase
from datetime import date 
  
def calculateAge(birthDate): 
    today = date.today() 
    age = today.year - birthDate.year -  ((today.month, today.day) < (birthDate.month, birthDate.day)) 
    return age 
      
print(calculateAge(date(2004, 10, 6)), "years") 


# Create your tests here.
