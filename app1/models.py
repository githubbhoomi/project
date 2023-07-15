from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.db.models import JSONField
from django.views.generic import ListView
from django.contrib.sessions.models import Session
# Create your models here.
class User(AbstractUser):
    is_princi = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    is_lecturer = models.BooleanField(default=False)
    is_clerk = models.BooleanField(default=False)
    is_librarian=models.BooleanField(default=False)
    class Meta:
        db_table = 'auth_user'
    def __str__(self):
        return self.first_name
class staff(models.Model):
    st=models.OneToOneField(User,on_delete=models.CASCADE)
    image=models.ImageField(upload_to='pics',default=False)
    def __str__(self):
        return self.st.first_name
class lecturer(models.Model):
    le=models.OneToOneField(User,on_delete=models.CASCADE)
    course=models.CharField(max_length=20,default=False)
    classes=models.CharField(max_length=20,default=False)
    image = models.ImageField(upload_to='pictures',default=False)
    def __str__(self):
        return self.le.first_name
class student(models.Model):
    s=models.OneToOneField(User,on_delete=models.CASCADE)
    total=models.FloatField(max_length=20,default=False)
    remain=models.CharField(max_length=20,null=True,blank=True,default=False)
    course=models.CharField(max_length=20,default=False)
    classes=models.CharField(max_length=20,default=False)
    image = models.ImageField(upload_to='studentpicture',default=False)
    def __str__(self):
        return self.s.first_name
class studentmark1(models.Model):
    s1=models.OneToOneField(student,on_delete=models.CASCADE)
    subject1=models.CharField(max_length=20,default=False)
    subject2=models.CharField(max_length=20,default=False)
    subject3=models.CharField(max_length=20,default=False)
    subject4=models.CharField(max_length=20,default=False)
    subject5=models.CharField(max_length=20,default=False)
    subject6=models.CharField(max_length=20,default=False)
    languages=models.CharField(max_length=20,default=False)
    def __str__(self):
        return self.s1.s.first_name
class studentmark2(models.Model):
    s1=models.OneToOneField(student,on_delete=models.CASCADE)
    subject1=models.CharField(max_length=20,default=False)
    subject2=models.CharField(max_length=20,default=False)
    subject3=models.CharField(max_length=20,default=False)
    subject4=models.CharField(max_length=20,default=False)
    subject5=models.CharField(max_length=20,default=False)
    subject6=models.CharField(max_length=20,default=False)
    languages=models.CharField(max_length=20,default=False)
    def __str__(self):
        return self.s1.s.first_name

class profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    forget_password_token=models.CharField(max_length=100)
    created_at=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.user.username
    
class subject(models.Model):
    data = JSONField(default=dict)

class appliedinfo(models.Model):
    name=models.CharField(max_length=100)
    lastname=models.CharField(max_length=100)
    contact_no=models.CharField(max_length=100)
    email_id=models.EmailField(max_length=100)
    gender=models.CharField(max_length=100)
    adharno=models.CharField(max_length=100)
    dob=models.CharField(max_length=100)
    place_of_birth=models.CharField(max_length=100)
    caste=models.CharField(max_length=100)
    category=models.CharField(max_length=100)
    parents_name=models.CharField(max_length=100)
    occupation=models.CharField(max_length=100)
    parent_no=models.CharField(max_length=100)
    income=models.CharField(max_length=100)
    address=models.CharField(max_length=100)
    course=models.CharField(max_length=100)
    language=models.CharField(max_length=100)
    regno=models.CharField(max_length=100)
    pay=models.CharField(max_length=100,default="")
    def __str__(self):
        return self.name
    


class displayappliedinfo(ListView):
    model=appliedinfo
    template_name='displayappinfo.html'
    
    def __str__(self):
        return self.name
 
class bookdetails(models.Model):
    bookid=models.CharField(primary_key=True,unique=True,max_length=100)
    bookimg=models.ImageField(upload_to='books',default=False)
    bookname=models.CharField(max_length=100)
    author=models.CharField(max_length=100)
    copies=models.IntegerField()
    total_copies=models.IntegerField()
    publication=models.CharField(max_length=100)
    type=models.CharField(max_length=100,default="Others")
    status=models.CharField(max_length=100,default="Available")
    borrower=models.CharField(max_length=100)
    def __str__(self):
        return self.bookname