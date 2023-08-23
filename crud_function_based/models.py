from django.db import models
from django.core.validators import RegexValidator

# Create your models here.
class Customer(models.Model):
    first_name      = models.CharField(max_length = 50, null=True)
    last_name       = models.CharField(max_length = 50, null=True)
    # picture         = models.ImageField()
    email           = models.EmailField(unique=True, max_length=100, blank=False)
    user_name   = models.CharField(max_length=50, unique=True, null = True, error_messages ={
                    "unique":"The User Name Field you entered is unique."
                    })
    phone_regex     = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number    = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    GENDER_SELECT = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    )
    gender = models.CharField(max_length=11,choices=GENDER_SELECT)
    dof				= models.DateField(null=True, blank=True)
    age 			= models.IntegerField(null=True)
    country         = models.CharField(max_length=50, null=True)
    city            = models.CharField(max_length=50, null=True)
    message         = models.TextField(default = 'Message...')
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.first_name
    
    
# class Profile(models.Model):
#      gender = models.CharField(choices=GENDER_CHOICES, max_length=128)