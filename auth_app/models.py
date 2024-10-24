from django.db import models
from django.contrib.auth.hashers import make_password

# Create your models here.      
class UserAuth(models.Model):
    email = models.EmailField(primary_key=True, max_length=255)
    name = models.CharField(max_length=100, default=None)
    password = models.CharField(max_length = 50)
    message = models.TextField()
     
    def __str__(self):
        return self.email
    
def set_password(raw_password):
    return make_password(raw_password)

    
def CheckPassword(password):
    special_char = ['/', '[', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', ',', '.', '?', ':', '{', '}', '|', '<', '>', ']']
    if len(password) < 8:
        return True
    elif " " in password.strip():
        return True
    else:
        upper_flag = 0
        lower_flag = 0
        digit_flag = 0
        special_flag = 0
        for char in password:
            if char in special_char:
                special_flag += 1
                continue
            elif char.isdigit():
                digit_flag += 1
                continue
            elif char.islower():
                lower_flag += 1
                continue
            elif char.isupper():
                upper_flag += 1
                continue
            else:
                continue
            
        if (upper_flag == 0 or lower_flag == 0) or (digit_flag == 0 or special_flag == 0):
            return True
    return False

