from django.db import models
from django.contrib.auth.models import User


# Create your models here.
COMPANY_CATEGORY = (
    ('Operations', 'Operations'),
    ('Marketing', 'Marketing'),
    ('IT', 'IT'),
    ('Management', 'Management'),
    ('Administration', 'Administration')
)

class Profile(models.Model):
    employee = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    role = models.CharField(max_length=200, null=True)
    role_department = models.CharField(max_length=100, choices=COMPANY_CATEGORY, null=True)
    image = models.ImageField(default='avatar.jpg', upload_to='Profile_Images')


    class Meta:
        verbose_name_plural = 'Profile'


    def __str__(self):
        return f'{self.employee.username}-Profile'

