from django.test import TestCase

# Create your tests here.
from django.contrib.auth.hashers import make_password, check_password

a = make_password("123456")
print(a)
a = check_password("123456", a)
print(a)

