import re, phonenumbers

def email(email):
   pat = "^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+\.[a-z]{1,3}$"
   if re.match(pat,email):
      return True
   return False

def phone(phone):
    s = phonenumbers.parse(phone, None)
    return phonenumbers.is_possible_number(s)
