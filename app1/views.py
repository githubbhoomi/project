from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth import authenticate,login,logout
from app1.models import staff,User,student,lecturer,studentmark1,studentmark2,appliedinfo,bookdetails
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import random
from django.contrib.sessions.models import Session
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.core.mail import send_mail
from datetime import datetime
from django.db.models import Max
from django.http import JsonResponse
from .models import subject 
from datetime import date
from django.conf import settings
from django.contrib.auth import get_user_model


def home(request):
    return render(request,"home.html")

def logout1(request):
    logout(request)
    return redirect('home')

def ssign(request):
    return render(request,"studentsignin.html")

def about(request):
    return render(request,"college.html")

def canteen(request):
    return render(request,"canteen.html")

def breakfast(request):
    return render(request,"breakfast.html")

def lunch(request):
    return render(request,"lunch.html")

def chat(request):
    return render(request,"chat.html")

def juice(request):
    return render(request,"juice.html")

def library(request):
    return render(request,"finallibrary.html")

def lab(request):
    return render(request,"finallab.html")

def plogin(request):
    return render(request,"plogin.html")
User = get_user_model()
def prlogin(request):
    # if request.user.is_anonymous:
    #     messages.success(request,"your a anonymous user")
    #     return render(request,"plogin.html")
    if request.method=="POST":
        email=request.POST.get("email")
        password=request.POST.get("password")
        if not email or not password:
            messages.success(request,"Both name and password is required")
            return render(request,"plogin.html")
        else:
            u=authenticate(username=email,password=password)
            if u is not None and u.is_princi:
                login(request,u)
                first_name = request.user.first_name
                email = request.user.email
                staff_obj = staff.objects.get(st=u)
                image = staff_obj.image
                user_count = User.objects.count()
                lecturer_count = lecturer.objects.count()
                staff_count =staff.objects.count()
                student_count = student.objects.count()
                context={
                    "user_count":user_count,
                    "lecturer_count":lecturer_count,
                    "staff_count":staff_count,
                    "student_count":student_count,
                    "firstname":first_name,
                    "image":image,
                    "email":email,

                }
                return render(request,"dashbord.html",context)
            elif u is not None and u.is_superuser:
                active_sessions = Session.objects.filter(expire_date__gte=timezone.now())
                session_keys = [session.session_key for session in active_sessions]
                activeuser = User.objects.filter(email__in=session_keys)
                print(activeuser)
                active_users_count = activeuser.count()
                logged_in_users = User.objects.filter(is_superuser=False, is_active=True)
                user_count = User.objects.count()
                lecturer_count = lecturer.objects.count()
                staff_count =staff.objects.count()
                student_count = student.objects.count()
                context={
                    "user_count":user_count,
                    "lecturer_count":lecturer_count,
                    "staff_count":staff_count,
                    "student_count":student_count,
                    "loggedusers":logged_in_users,
                    "activeuser":activeuser,
                    "active_users_count":active_users_count,
                }
                return render(request,"superdashboard.html",context)
            elif u is not None and u.is_staff:
                login(request,u)
                return render(request,"studentsignin.html")
            elif u is not None and u.is_student:
                login(request,u)
                return render(request,"studentrights.html")
            elif u is not None and u.is_lecturer:
                login(request,u)   
                l=request.user
                ls=lecturer.objects.get(le=l)
                classes=ls.classes
                course=ls.course 
                image=ls.image
                name=ls.le.first_name
                context={
                    "classes":classes,
                    "course":course,
                    "name":name,
                    "image":image
                }          
                return render(request,"my_form.html",context)
            elif u is not None and u.is_librarian==True:
                print("librarian")
                login(request,u)
                return render(request,'libhome.html')
            else:
                messages.success(request,"not an authorized user")
                return render(request,"plogin.html")
       

def accountantadd(request):
    if request.method=="POST":
        aname=request.POST.get("aname")
        aemail=request.POST.get("aemail")
        apassword=request.POST.get("apassword")
        rpassword=request.POST.get("rpassword")
        image = request.FILES['image']
        type=request.POST.get("type")
        is_staff = 'is_accountant' in type
        is_clerk = 'is_clerk' in type
        is_librarian='is_librarian' in type
        if apassword!=rpassword:
            messages.success(request,"Both password should be same")
            return render(request,"accountantsignin.html")
        u=User.objects.create_user(username=aemail,email=aemail,password=apassword,is_staff=is_staff,is_clerk=is_clerk,is_librarian=is_librarian)
        u.first_name=aname
        u.save()
        s=staff(st=u,image=image)
        s.save()
        if u.is_staff==True:
            messages.success(request,"Accountant details saved")
            return render(request,"accountantsignin.html")
        elif u.is_clerk==True:
            messages.success(request,"Clerk details saved")
            return render(request,"accountantsignin.html")
        elif u.is_librarian==True:
            messages.success(request,"Librarian details saved")
            return render(request,"accountantsignin.html")

def deletelecturer1(request):
    if request.method=="POST":
            email=request.POST.get("demail")
            if User.objects.filter(email=email).first():
                user = User.objects.get(email=email)
                user.delete()
                messages.success(request,f"{user} record deleted")
                return redirect(back)
            else:
                messages.success(request,"record does not exist")
                return redirect(back)

def delete_student(request):
    if request.method=="POST":
        email=request.POST.get("demail")
        if User.objects.filter(email=email).first():
            user = User.objects.get(email=email)
            user.delete()
            messages.success(request,f"{user} record deleted")
            return redirect(back)
        else:
            messages.success(request,"record does not exist")
            return redirect(back)

def deletepassstd(request):
    if request.method=="POST":
        classes=request.POST.get("classes")
        course=request.POST.get("course")
        students = student.objects.filter(classes=classes, course=course)
        if students.exists():
            student_emails = students.values_list('s__email', flat=True)
            s=subject.objects.filter(data__course=course,data__classes=classes)
            s1=studentmark1.objects.filter(s1__s__email__in=student_emails)
            if s.exists() and s1.exists():
                    s.delete()
                    s1.delete()
            for studen in students:
                user = studen.s
                user.delete()
            messages.success(request,f"students at {classes} class and {course} course records deleted")
            return redirect(back)
        else:
            messages.success(request,f"students at {classes} class and {course} course records does not exists")
            return redirect(back)
    
def deletepassstd1(request):
    if request.method=="POST":
        classes=request.POST.get("classes")
        course=request.POST.get("course")
        students = student.objects.filter(classes=classes, course=course)
        if students.exists():
            student_emails = students.values_list('s__email', flat=True)
            s=subject.objects.filter(data__course=course,data__classes=classes)
            s1=studentmark1.objects.filter(s1__s__email__in=student_emails)
            if s.exists() and s1.exists():
                    s.delete()
                    s1.delete()
            for studen in students:
                user = studen.s
                user.delete()
            messages.success(request,f"students at {classes} class and {course} course records deleted")
            return redirect(backadmin)
        else:
            messages.success(request,f"students at {classes} class and {course} course records does not exists")
            return redirect(backadmin)
    
def delete_student11(request):
    if request.method=="POST":
        email=request.POST.get("demail")
        if User.objects.filter(email=email).first():
            user = User.objects.get(email=email)
            user.delete()
            messages.success(request,f"{user} record deleted")
            return redirect(backadmin)
        else:
            messages.success(request,"record does not exist")
            return redirect(backadmin)
            
def deletelecturer11(request):
    if request.method=="POST":
            email=request.POST.get("demail")
            if User.objects.filter(email=email).first():
                user = User.objects.get(email=email)
                user.delete()
                messages.success(request,f"{user} record deleted")
                return redirect(backadmin)
            else:
                messages.success(request,"record does not exist")
                return redirect(backadmin)
            
def studentadd(request):
    if request.method=="POST":
        if 'b1' in request.POST:
            sname=request.POST.get("aname")
            course=request.POST.get("course",None)
            classes=request.POST.get("classes",None)
            semail=request.POST.get("semail")
            spassword=request.POST.get("apassword")
            rpassword=request.POST.get("rpassword")
            image = request.FILES['image'] 
            if spassword!=rpassword:
                messages.success(request,"Both password should be same")
                return render(request,"studentsignin.html")
            if not sname or not course or not classes or not semail or not spassword or not image:
                messages.success(request,"Please enter all the details...!")
                return render(request,"studentsignin.html")
            if User.objects.filter(email=semail).first():
                messages.success(request,"email is already taken")
                return render(request,"studentsignin.html")
            u=User.objects.create_user(username=semail,email=semail,password=spassword,is_student=True)
            u.first_name=sname
            u.save()
            s=student(s=u,course=course,classes=classes,image=image)
            s.save()
            login(request,u)
            l=len(User.objects.all())
            k=l-1
            name=User.objects.all()[k].first_name
            return render(request, 'paydetail.html',{'std':name})
                  
def paydet(request):
        if request.method=="POST":
            total=float(request.POST.get('total'))
            paid=float(request.POST.get('pay'))
            s = request.user
            s, created = student.objects.get_or_create(s=s)
            s.total = total
            s.remain=s.total
            if s.remain<=0:
                messages.success(request,"Fees fully paid")
                return render(request,"paydetail.html")
            p=s.remain-paid
            s.remain = p
            s.save()
            total = s.total
            remain = s.remain
            name = s.s.first_name
            course = s.course
            classes = s.classes
            date1=str(date.today())
            context = {'name' : name,
            'total': total,
            'remain':remain,
            'paid':paid,
            'date1':date1,
            'course':course,
            'classes':classes
            }
            print(s.s.email)
            msg = f" {name} paid amount Rs.{paid} and the remaining fees is {remain} "
            subject='Fees Payment'
            message=f'{msg}'
            email_from= settings.EMAIL_HOST_USER
            recipeient_list=[s.s.email]
            send_mail(subject,message,email_from,recipeient_list)
            messages.success(request, f"Amount paid: Rs.{paid} by {name}") 
            return render(request, 'areceipt.html',context)
        
def extra(request):
        user = request.user
        try:
            student_obj = student.objects.get(s=user)
            total = student_obj.total
            remain = student_obj.remain
            name = student_obj.s.first_name
        except student.DoesNotExist:
            total = None
        context = {'name' : name,
            'total': total,
            'remain':remain}
        return render(request, 'paydetail1.html',context)

def spaydet(request):
        if request.method=="POST":
            total=float(request.POST.get('total'))
            paid=float(request.POST.get('pay'))
            s = request.user
            s, created = student.objects.get_or_create(s=s)
            k=float(s.remain)
            if k<=0:
                messages.success(request,"Fees fully paid --> 0:)")
                return render(request,"paydetail1.html")
            p=k-paid
            s.remain = p
            s.save()
            total = s.total
            remain = s.remain
            name = s.s.first_name
            course = s.course
            classes = s.classes
            date1=str(date.today())
            context = {'name' : name,
            'total': total,
            'remain':remain,
            'paid':paid,
            'date1':date1,
            'course':course,
            'classes':classes
            }
            print(s.s.email)
            msg = f" {name} paid amount Rs.{paid} and the remaining fees is {remain} "
            subject='Fees Payment'
            message=f'{msg}'
            email_from= settings.EMAIL_HOST_USER
            recipeient_list=[s.s.email]
            send_mail(subject,message,email_from,recipeient_list)
            messages.success(request, f"Amount paid: Rs.{paid} by {name}") 
            return render(request, 'receipt.html',context)

def forgot(request):
    return render(request,"forgot.html")

def sendme(request):
    if request.method=="POST":
        email=request.POST.get('email')
        u=User.objects.filter(email=email).first()
        if u is not None :
            login(request,u)
            otp = ''.join([str(random.randint(0, 9)) for _ in range(6)])
            subject='OTP for change password'
            message=f'Hi ,your otp is {otp}'
            email_from= settings.EMAIL_HOST_USER
            recipeient_list=[email]
            send_mail(subject,message,email_from,recipeient_list)
            messages.success(request,"Email sent")
            return render(request, 'otp.html', {'otp': otp})
        else:
            messages.success(request,"User name does not exists..!")
            return render(request,"forgot.html")
                   
def checkotp(request):
    if request.method=="POST":
        gotp=request.POST.get("eotp")
        otp = request.POST.get("otp")
        print(gotp,otp)
        if otp==gotp:
            return render(request,"change-password.html")
        else:
            messages.success(request,"OTP does not match..?")
            return render(request,'otp.html')
        
def changeit(request):
    u=request.user
    if request.method=="POST":
        npsw=request.POST.get("npas")
        rnpaw=request.POST.get("rnpas")
        if npsw!=rnpaw:
            messages.success(request,"Password does not match")
            return render(request,"change-password.html")
        else:
            u.set_password(npsw)
            u.save()
            messages.success(request,"Password changed(:")
            return render(request,"plogin.html")

def signinn(request):
    return render(request,"studentsignin.html")

def asign(request):
    return render(request,"accountantsignin.html")

def addlect1(request):
    return render(request,"lecturersignin1.html")

def backadmin(request):
    active_sessions = Session.objects.filter(expire_date__gte=timezone.now())
    session_keys = [session.session_key for session in active_sessions]
    activeuser = User.objects.filter(email__in=session_keys)
    active_users_count = activeuser.count()
    logged_in_users = User.objects.filter(is_superuser=False, is_active=True)
    user_count = User.objects.count()
    lecturer_count = lecturer.objects.count()
    staff_count =staff.objects.count()
    student_count = student.objects.count()
    context={
                    "user_count":user_count,
                    "lecturer_count":lecturer_count,
                    "staff_count":staff_count,
                    "student_count":student_count,
                    "loggedusers":logged_in_users,
                    "activeuser":activeuser,
                    "active_users_count":active_users_count,
    }
    return render(request,"superdashboard.html",context)

               
def addstaff1(request):
    return render(request,"accountantsignin1.html")  
    
def student_view3(request, course=None, classes=None):
    students = student.objects.filter(s__is_student=True, course=course, classes=classes)
    context = {
        'students': students,
    }
    return render(request, 'studentinformation_princi1.html',context)

def addlect(request):
    return render(request,"lecturersignin.html")

def addstaff(request):
    return render(request,"accountantsignin.html") 


def lectureradd(request):
        if request.method=="POST":
            aname=request.POST.get("aname")
            aemail=request.POST.get("aemail")
            apassword=request.POST.get("apassword")
            rpassword=request.POST.get("rpassword")
            course=request.POST.get("course","")
            classes=request.POST.get("classes","")
            image = request.FILES['image']
            if apassword!=rpassword:
                messages.success(request,"Both password should be same")
                return render(request,"lecturersignin1.html")
            u=User.objects.create_user(username=aemail,email=aemail,password=apassword,is_lecturer=True)
            u.first_name=aname
            u.save()
            s=lecturer(le=u,classes=classes,course=course,image=image)
            s.save()
            messages.success(request,"Lecturer details saved")
            return render(request,"lecturersignin.html")

def lectureradd1(request):
        if request.method=="POST":
            aname=request.POST.get("aname")
            aemail=request.POST.get("aemail")
            apassword=request.POST.get("apassword")
            rpassword=request.POST.get("rpassword")
            course=request.POST.get("course","")
            classes=request.POST.get("classes","")
            image = request.FILES['image']
            if apassword!=rpassword:
                messages.success(request,"Both password should be same")
                return render(request,"lecturersignin1.html")
            u=User.objects.create_user(username=aemail,email=aemail,password=apassword,is_lecturer=True)
            u.first_name=aname
            u.save()
            s=lecturer(le=u,classes=classes,course=course,image=image)
            s.save()
            messages.success(request,"Lecturer details saved")
            return render(request,"lecturersignin1.html")
    

def accountantadd1(request):
    if request.method=="POST":
        aname=request.POST.get("aname")
        aemail=request.POST.get("aemail")
        apassword=request.POST.get("apassword")
        rpassword=request.POST.get("rpassword")
        image = request.FILES['image']
        type=request.POST.get("type")
        is_staff = 'is_accountant' in type
        is_clerk = 'is_clerk' in type
        is_librarian='is_librarian' in type
        is_princi='is_princi' in type
        if apassword!=rpassword:
            messages.success(request,"Both password should be same")
            return render(request,"accountantsignin1.html")
        u=User.objects.create_user(username=aemail,email=aemail,password=apassword,is_staff=is_staff,is_clerk=is_clerk,is_librarian=is_librarian,is_princi=is_princi)
        u.first_name=aname
        u.save()
        s=staff(st=u,image=image)
        s.save()
        if u.is_staff==True:
            messages.success(request,"Accountant details saved")
            return render(request,"accountantsignin1.html")
        elif u.is_clerk==True:
            messages.success(request,"Clerk details saved")
            return render(request,"accountantsignin1.html")
        elif u.is_librarian==True:
            messages.success(request,"Librarian details saved")
            return render(request,"accountantsignin1.html")
        elif u.is_princi==True:
            messages.success(request,"Principal details saved")
            return render(request,"accountantsignin1.html")
    
def lviewbca(request, course=None):
    lecturerinfo_bca = lecturer.objects.filter(le__is_lecturer=True,course=course)
    context = {
        'lecturerinfo_bca': lecturerinfo_bca,
    }
    return render(request, 'lecturerprofile.html',context)


def staffsview(request,type=None):
    if "is_staff" in type:
        staffview = staff.objects.filter(st__is_staff=True)
        context = {
            'staffsview': staffview,
        }
        return render(request, 'lecturerprofile.html',context)
    elif "is_clerk" in type:
        staffview = staff.objects.filter(st__is_clerk=True)
        context = {
            'staffsview': staffview,
        }
        return render(request, 'lecturerprofile.html',context)
    elif "is_librarian" in type:
        staffview = staff.objects.filter(st__is_librarian=True)
        context = {
            'staffsview': staffview,
        }
        return render(request, 'lecturerprofile.html',context)
    elif "is_princi" in type:
            staffview = staff.objects.filter(st__is_princi=True)
            context = {
                'staffsview': staffview,
            }
            return render(request, 'lecturerprofile.html',context)



def student_view1(request, course=None, classes=None):
    students = student.objects.filter(s__is_student=True, course=course, classes=classes)
    context = {
        'students': students,
    }
    return render(request, 'studentinformation.html',context)

def student_view2(request, course=None, classes=None):
    students = student.objects.filter(s__is_student=True, course=course, classes=classes)
    context = {
        'students': students,
    }
    return render(request, 'studentinformation_princi.html',context)

@login_required
def back(request):
    u=request.user
    first_name = request.user.first_name
    email = request.user.email
    staff_obj = staff.objects.get(st=u)
    image = staff_obj.image
    user_count = User.objects.count()
    lecturer_count = lecturer.objects.count()
    staff_count =staff.objects.count()
    student_count = student.objects.count()
    context={
                    "user_count":user_count,
                    "lecturer_count":lecturer_count,
                    "staff_count":staff_count,
                    "student_count":student_count,
                    "firstname":first_name,
                    "image":image,
                    "email":email,

                }
    return render(request,"dashbord.html",context)

def student_view(request, course=None, classes=None):
    students = student.objects.filter(s__is_student=True, course=course, classes=classes)
    context = {
        'students': students,
    }
    return render(request, 'sview.html', context)
def student_view4(request, course=None, classes=None):
    students = student.objects.filter(s__is_student=True, course=course, classes=classes)
    context = {
        'students': students,
    }
    return render(request, 'sview1.html', context)
def student_view5(request, course=None, classes=None):
    students = student.objects.filter(s__is_student=True, course=course, classes=classes)
    context = {
        'students': students,
    }
    return render(request, 'sview2.html', context)
def student_view6(request, course=None, classes=None):
    students = student.objects.filter(s__is_student=True, course=course, classes=classes)
    context = {
        'students': students,
    }
    return render(request, 'sview3.html', context)

def stdinfo(request):
    return render(request,"studentsignin.html")

def lsign(request):
    return render(request,"lecturersignin.html")

@login_required 
def my_view(request):
    if request.method=="POST":
        btn1=request.POST.get("btn1"," ")
        internals=request.POST.get("internals")
        s1=request.POST.get("subject1")
        s2=request.POST.get("subject2")
        s3=request.POST.get("subject3")
        s4=request.POST.get("subject4")
        s5=request.POST.get("subject5")
        s6=request.POST.get("subject6")
        lg=request.POST.get("language")
        classes=request.POST.get("classes")
        course=request.POST.get("course")
        s11=request.user
        try:
            ss=lecturer.objects.get(le=s11)
            classes=ss.classes
            course=ss.course
        except:
            messages.success(request,f"No students with the {classes} {course} class.")
            return render(request,'my_form.html')
        if "Submit" in btn1:
            if not internals:
                messages.success(request,"enter all data")
                return render(request,'my_form.html')
            subb = subject.objects.filter(data__classes=classes, data__course=course, data__internals=internals)
            if subb.exists():
                messages.success(request,"Marks are already sent")
                return render(request,'my_form.html')
            else:
                context = {
                    'subject1':s1,
                    'subject2':s2,
                    'subject3':s3,
                    'subject4':s4,
                    'subject5':s5,
                    'subject6':s6,
                    'subject7':lg,
                    "classes":classes,
                    "course":course,
                    "internals":internals
                    }
                students = student.objects.filter(course=course,classes=classes)
                context['students'] = students
                if internals=="I Internal":
                    return render(request, 'emark.html',context)
                else:
                    return render(request, 'emark.html',context)
                
def marksviewall(request, course=None, classes=None, internals=None):
    subs = subject.objects.filter(data__classes=classes, data__course=course, data__internals=internals)
    if internals == "I Internal":
        students = student.objects.filter(course=course, classes=classes)
        studentsmark = studentmark1.objects.filter(s1__in=students)
        if studentsmark.exists():
            context = {
                'sub': subs,
                'sub1': studentsmark,
                'students': students,
                'classes': classes,
                'course': course,
                'internals': internals,
            }
            return render(request, 'showmark.html', context)
        else:
            messages.success(request, ' Internal marks not found')  
            return render(request, "my_form.html")
    elif internals == "II Internal":
        students = student.objects.filter(course=course, classes=classes)
        studentsmark = studentmark2.objects.filter(s1__in=students)
        if studentsmark.exists():
            context = {
                'sub': subs,
                'sub1': studentsmark,
                'students': students,
                'classes': classes,
                'course': course,
                'internals': internals,
            }
            return render(request, 'showmark.html', context)
        else:
            messages.success(request, 'Internal marks not found')  
            return render(request, "my_form.html")
        
def marks(request):
    # if request.user.is_anonymous:
    #     messages.success(request,"your a not login...please login")
    #     return render(request,"plogin.html")
    if request.method == "POST":
        btn=request.POST.get("btn","")
        if "save" in btn:
            classes=request.POST.get("classes")
            course=request.POST.get("course")
            internals=request.POST.get("internals")
            sub1=request.POST.get("subject1")
            sub2=request.POST.get("subject2")
            sub3=request.POST.get("subject3")
            sub4=request.POST.get("subject4")
            sub5=request.POST.get("subject5")
            sub6=request.POST.get("subject6")
            sub7=request.POST.get("subject7")
            my_instance = subject()
            my_instance.data = {
                "subject1": sub1,
                "subject2": sub2,
                "subject3": sub3,
                "subject4": sub4,
                "subject5": sub5,
                "subject6": sub6,
                "language": sub7,
                "classes":classes,
                "course":course,
                "internals":internals,
                }
            students = student.objects.filter(classes=classes,course=course)
            if internals=="I Internal":
                for student_obj in students:
                    mark1 = request.POST.get(f"mark1_{student_obj.s.email}")
                    mark2 = request.POST.get(f"mark2_{student_obj.s.email}")
                    mark3 = request.POST.get(f"mark3_{student_obj.s.email}")
                    mark4 = request.POST.get(f"mark4_{student_obj.s.email}")
                    mark5 = request.POST.get(f"mark5_{student_obj.s.email}")
                    mark6 = request.POST.get(f"mark6_{student_obj.s.email}")
                    mark7 = request.POST.get(f"mark7_{student_obj.s.email}")
                    try:
                        student_mark = studentmark1.objects.get(s1_id=student_obj.id)
                    except studentmark1.DoesNotExist:
                        student_mark = studentmark1(s1_id=student_obj.id)

                    if mark1:
                        student_mark.subject1 = mark1
                    if mark2:
                        student_mark.subject2 = mark2
                    if mark3:
                        student_mark.subject3 = mark3
                    if mark4:
                        student_mark.subject4 = mark4
                    if mark5:
                        student_mark.subject5 = mark5
                    if mark6:
                        student_mark.subject6 = mark6
                    if mark7:
                        student_mark.languages = mark7
                    my_instance.save()    
                    student_mark.save()
                classes=classes
                course=course
                internal=internals
                url = reverse('sendmailmark') + f"?classes={classes}&course={course}&internal={internal}"
                context = {
                    "message": "Marks saved successfully.If you want to send marks in email click open url",
                    "url": url
                }
                return render(request, "messegelink.html", context)

            elif internals=="II Internal":
                for student_obj in students:
                    mark1 = request.POST.get(f"mark1_{student_obj.s.email}")
                    mark2 = request.POST.get(f"mark2_{student_obj.s.email}")
                    mark3 = request.POST.get(f"mark3_{student_obj.s.email}")
                    mark4 = request.POST.get(f"mark4_{student_obj.s.email}")
                    mark5 = request.POST.get(f"mark5_{student_obj.s.email}")
                    mark6 = request.POST.get(f"mark6_{student_obj.s.email}")
                    mark7 = request.POST.get(f"mark7_{student_obj.s.email}")
                    try:
                        student_mark = studentmark2.objects.get(s1_id=student_obj.id)
                    except studentmark2.DoesNotExist:
                        student_mark = studentmark2(s1_id=student_obj.id)

                    if mark1:
                        student_mark.subject1 = mark1
                    if mark2:
                        student_mark.subject2 = mark2
                    if mark3:
                        student_mark.subject3 = mark3
                    if mark4:
                        student_mark.subject4 = mark4
                    if mark5:
                        student_mark.subject5 = mark5
                    if mark6:
                        student_mark.subject6 = mark6
                    if mark7:
                        student_mark.languages = mark7
                    my_instance.save()  
                    student_mark.save()
                classes=classes
                course=course
                internal=internals
                url = reverse('sendmailmark') + f"?classes={classes}&course={course}&internal={internal}"
                context = {
                    "message": "Marks saved successfully.If you want to send marks in email click open url",
                    "url": url
                }
                return render(request, "messegelink.html", context)
            
def sendmail(request):
    if request.method=="POST":
        classes=request.POST.get("classes")
        course=request.POST.get("course")
        internals=request.POST.get("internals")
        sub1=request.POST.get("subject1")
        sub2=request.POST.get("subject2")
        sub3=request.POST.get("subject3")
        sub4=request.POST.get("subject4")
        sub5=request.POST.get("subject5")
        sub6=request.POST.get("subject6")
        sub7=request.POST.get("subject7")
        students = student.objects.filter(classes=classes,course=course)
        if internals == "I Internal":
                for student_obj in students:
                    email = student_obj.s.email
                    mark1 = request.POST.get(f"mark1_{student_obj.s.email}")
                    mark2 = request.POST.get(f"mark2_{student_obj.s.email}")
                    mark3 = request.POST.get(f"mark3_{student_obj.s.email}")
                    mark4 = request.POST.get(f"mark4_{student_obj.s.email}")
                    mark5 = request.POST.get(f"mark5_{student_obj.s.email}")
                    mark6 = request.POST.get(f"mark6_{student_obj.s.email}")
                    mark7 = request.POST.get(f"mark7_{student_obj.s.email}")
                    try:
                        student_mark = studentmark1.objects.get(s1_id=student_obj.id)
                    except studentmark1.DoesNotExist:
                        student_mark = studentmark1(s1_id=student_obj.id)

                    if mark1:
                        student_mark.subject1 = mark1
                    if mark2:
                        student_mark.subject2 = mark2
                    if mark3:
                        student_mark.subject3 = mark3
                    if mark4:
                        student_mark.subject4 = mark4
                    if mark5:
                        student_mark.subject5 = mark5
                    if mark6:
                        student_mark.subject6 = mark6
                    if mark7:
                        student_mark.languages = mark7
                    mark = f"first internal marks:{sub1}:{mark1},{sub2}:{mark2},{sub3}:{mark3},{sub4}:{mark4},{sub5}:{mark5},{sub6}:{mark6},{sub7}:{mark7}"
                    subjects='I intternal marks'
                    message=f'{mark}'
                    email_from= settings.EMAIL_HOST_USER
                    recipeient_list=[email]
                    send_mail(subjects,message,email_from,recipeient_list)
                    context={
                        "classes":classes,
                        "course":course
                    }
                messages.success(request," I internal marks sent in email ")
                return render(request,"my_form.html",context)
        elif internals == "II Internal":
                for student_obj in students:
                    email = student_obj.s.email
                    mark1 = request.POST.get(f"mark1_{student_obj.s.email}")
                    mark2 = request.POST.get(f"mark2_{student_obj.s.email}")
                    mark3 = request.POST.get(f"mark3_{student_obj.s.email}")
                    mark4 = request.POST.get(f"mark4_{student_obj.s.email}")
                    mark5 = request.POST.get(f"mark5_{student_obj.s.email}")
                    mark6 = request.POST.get(f"mark6_{student_obj.s.email}")
                    mark7 = request.POST.get(f"mark7_{student_obj.s.email}")
                    print(mark1,mark2,mark3,mark4,mark5,mark6,mark7)
                    try:
                        student_mark = studentmark2.objects.get(s1_id=student_obj.id)
                    except studentmark1.DoesNotExist:
                        student_mark = studentmark2(s1_id=student_obj.id)

                    if mark1:
                        student_mark.subject1 = mark1
                    if mark2:
                        student_mark.subject2 = mark2
                    if mark3:
                        student_mark.subject3 = mark3
                    if mark4:
                        student_mark.subject4 = mark4
                    if mark5:
                        student_mark.subject5 = mark5
                    if mark6:
                        student_mark.subject6 = mark6
                    if mark7:
                        student_mark.languages = mark7
                    mark = f"first internal marks:{sub1}:{mark1},{sub2}:{mark2},{sub3}:{mark3},{sub4}:{mark4},{sub5}:{mark5},{sub6}:{mark6},{sub7}:{mark7}"
                    subjects='I intternal marks'
                    message=f'{mark}'
                    email_from= settings.EMAIL_HOST_USER
                    recipeient_list=[email]
                    send_mail(subjects,message,email_from,recipeient_list)
                    context={
                        "classes":classes,
                        "course":course
                    }
                messages.success(request," IT internal marks sent in email ")
                return render(request,"my_form.html",context)
            
def sendmailmark(request):
    classes = request.GET.get('classes')
    course = request.GET.get('course')
    internal = request.GET.get('internal')
    sub = subject.objects.filter(data__classes=classes, data__course=course, data__internals=internal)  
    if internal=="I Internal":
        students = student.objects.filter(course=course, classes=classes)
        studentsmark = studentmark1.objects.filter(s1__in=students)
        if studentsmark.exists():
            context = {
                'sub': sub,
                'sub1': studentsmark,
                'students': students,
                'classes': classes,
                'course': course,
                'internals': internal,
            }
            return render(request, 'showmarkforsendmail.html', context)
        return render(request, "emark.html", context)
    elif internal=="II Internal":
        students = student.objects.filter(course=course, classes=classes)
        studentsmark = studentmark2.objects.filter(s1__in=students)
        if studentsmark.exists():
            context = {
                'sub': sub,
                'sub1': studentsmark,
                'students': students,
                'classes': classes,
                'course': course,
                'internals': internal,
            }
            return render(request, 'showmarkforsendmail.html', context)
        return render(request, "emark.html", context)
def delete_marks(request):
    if request.method=="POST":
        classes = request.POST.get("classes")
        course = request.POST.get("course")
        internal=request.POST.get("internals")
        if internal=="I Internal":
            student_instances = student.objects.filter(classes=classes, course=course)
            student_emails = student_instances.values_list('s__email', flat=True)
            s=subject.objects.filter(data__course=course,data__classes=classes,data__internals=internal)
            s1=studentmark1.objects.filter(s1__s__email__in=student_emails)
            if s.exists() and s1.exists():
                s.delete()
                s1.delete()
                messages.success(request,"Record deleted..")
                return render(request,"my_form.html")
            else:
                messages.success(request,"Record does not exists..")
                return render(request,"my_form.html")
        elif internal=="II Internal":
            student_instances = student.objects.filter(classes=classes, course=course)
            student_emails = student_instances.values_list('s__email', flat=True)
            s=subject.objects.filter(data__course=course,data__classes=classes,data__internals=internal)
            s1=studentmark2.objects.filter(s1__s__email__in=student_emails)
            if s.exists() and s1.exists():
                s.delete()
                s1.delete()
                messages.success(request,"Record deleted..")
                return render(request,"my_form.html")
            else:
                messages.success(request,"Record does not exists..")
                return render(request,"my_form.html")
        
@login_required
def student_view_marks(request,internal=None):
    s=request.user
    email=s.email
    name=s.first_name
    s1=student.objects.get(s=s)
    classs=s1.classes
    cour=s1.course
    if internal=="I Internal":
            try:
                subs = subject.objects.filter(data__classes=classs, data__course=cour,data__internals=internal)
                s=studentmark1.objects.get(s1=s1)
                context={
                    'sub': subs,
                    'sub1': s,
                    'students': s1,
                    'name':name
                }
                return render(request,"student_view_mark.html",context)
            except:
                messages.success(request," I Internal marks are not found")
                return render(request,"studentrights.html")
    elif internal=="II Internal":
            try:
                subs = subject.objects.filter(data__classes=classs, data__course=cour,data__internals=internal)
                s=studentmark2.objects.get(s1=s1)
                context={
                    'sub': subs,
                    'sub1': s,
                    'students': s1,
                    'name':name
                }
                return render(request,"student_view_mark.html",context)
            except:
                messages.success(request,"II Internal marks are not found")
                return render(request,"studentrights.html")

def update_marks(request):
    if request.method == "POST":
        classes = request.POST.get("classes")
        course = request.POST.get("course")
        internals = request.POST.get("internals")
        sub = subject.objects.filter(data__classes=classes, data__course=course, data__internals=internals)
        if sub.exists():
            students = student.objects.filter(classes=classes, course=course)
            for subject_obj in sub:
                subject_data = subject_obj.data
                subject1 = subject_data.get('subject1') 
                subject2 = subject_data.get('subject2')
                subject3 = subject_data.get('subject3')
                subject4 = subject_data.get('subject4')
                subject5 = subject_data.get('subject5')
                subject6 = subject_data.get('subject6')
                subject7 = subject_data.get('language')

            if internals=="I Internal":
                marks = studentmark1.objects.filter(s1__in=students)
                context = {
                    "subject1":subject1,
                    "subject2":subject2,
                    "subject3":subject3,
                    "subject4":subject4,
                    "subject5":subject5,
                    "subject6":subject6,
                    "subject7":subject7,
                    "students": students,
                    "marks": marks,
                    "internals":internals,
                    "classes":classes,
                    "course":course
                }
                return render(request, "emarkupdate.html", context)
            elif internals == "II Internal":
                marks = studentmark2.objects.filter(s1__in=students)
                context = {
                    "subject1":subject1,
                    "subject2":subject2,
                    "subject3":subject3,
                    "subject4":subject4,
                    "subject5":subject5,
                    "subject6":subject6,
                    "subject7":subject7,
                    "students": students,
                    "marks": marks,
                    "internals":internals,
                    "classes":classes,
                    "course":course
                }
                return render(request, "emarkupdate.html", context)
        else:
            messages.success(request,"Marks not found")
            return render(request,"my_form.html")
        
def updatemore(request):
    classes = request.GET.get('classes')
    course = request.GET.get('course')
    internal = request.GET.get('internal')
    sub = subject.objects.filter(data__classes=classes, data__course=course, data__internals=internal)  
    if sub.exists():
        students = student.objects.filter(classes=classes, course=course)
        for subject_obj in sub:
            subject_data = subject_obj.data
            subject1 = subject_data.get('subject1') 
            subject2 = subject_data.get('subject2')
            subject3 = subject_data.get('subject3')
            subject4 = subject_data.get('subject4')
            subject5 = subject_data.get('subject5')
            subject6 = subject_data.get('subject6')
            subject7 = subject_data.get('language')

    if internal=="I Internal":
        marks = studentmark1.objects.filter(s1__in=students)
        context = {
                    "subject1":subject1,
                    "subject2":subject2,
                    "subject3":subject3,
                    "subject4":subject4,
                    "subject5":subject5,
                    "subject6":subject6,
                    "subject7":subject7,
                    "students": students,
                    "marks": marks,
                    "internals":internal,
                    "classes":classes,
                    "course":course
            }
        return render(request, "emarkupdate.html", context)
    elif internal=="II Internal":
        marks = studentmark2.objects.filter(s1__in=students)
        context = {
                    "subject1":subject1,
                    "subject2":subject2,
                    "subject3":subject3,
                    "subject4":subject4,
                    "subject5":subject5,
                    "subject6":subject6,
                    "subject7":subject7,
                    "students": students,
                    "marks": marks,
                    "internals":internal,
                    "classes":classes,
                    "course":course
            }
        return render(request, "emarkupdate.html", context)
    else:
            messages.success(request,"Marks not found")
            return render(request,"my_form.html")
    
def updateit(request):
    if request.method=="POST":
        btn=request.POST.get("btn1"," ")
        if "edit" in btn:
            s1=request.POST.get("sub1")
            s2=request.POST.get("sub2")
            s3=request.POST.get("sub3")
            s4=request.POST.get("sub4")
            s5=request.POST.get("sub5")
            s6=request.POST.get("sub6")
            s7=request.POST.get("sub7")
            email=request.POST.get("email")
            classes=request.POST.get("classes")
            course=request.POST.get("course")
            internal=request.POST.get("internal")
            if internal=="I Internal":
                d=studentmark1.objects.filter(s1__s__email=email)
                for obj in d:
                    obj.subject1 = s1
                    obj.subject2 = s2
                    obj.subject3 = s3
                    obj.subject4 = s4
                    obj.subject5 = s5
                    obj.subject6 = s6
                    obj.languages =s7
                    obj.save()
                classes=classes
                course=course
                internal=internal
                url = reverse('updatemore') + f"?classes={classes}&course={course}&internal={internal}"
                context = {
                    "message": "Marks saved successfully.If you want to send marks in email click open url",
                    "url": url
                }
                return render(request, "messegelink.html", context)
            elif internal=="II Internal":
                d=studentmark2.objects.filter(s1__s__email=email)
                for obj in d:
                    obj.subject1 = s1
                    obj.subject2 = s2
                    obj.subject3 = s3
                    obj.subject4 = s4
                    obj.subject5 = s5
                    obj.subject6 = s6
                    obj.languages =s7
                    obj.save()
                classes=classes
                course=course
                internal=internal
                url = reverse('updatemore') + f"?classes={classes}&course={course}&internal={internal}"
                context = {
                    "message": "Marks saved successfully.If you want to send marks in email click open url",
                    "url": url
                }
                return render(request, "messegelink.html", context)
        elif "sendmail" in btn:
            s1=request.POST.get("sub1")
            s2=request.POST.get("sub2")
            s3=request.POST.get("sub3")
            s4=request.POST.get("sub4")
            s5=request.POST.get("sub5")
            s6=request.POST.get("sub6")
            s7=request.POST.get("sub7")
            email=request.POST.get("email")
            internal=request.POST.get("internal")
            classes=request.POST.get("classes")
            course=request.POST.get("course")
            if internal=="I Internal":
                sub = subject.objects.filter(data__classes=classes, data__course=course, data__internals=internal)
                for subject_obj in sub:
                    subject_data = subject_obj.data
                    subject1 = subject_data.get('subject1') 
                    subject2 = subject_data.get('subject2')
                    subject3 = subject_data.get('subject3')
                    subject4 = subject_data.get('subject4')
                    subject5 = subject_data.get('subject5')
                    subject6 = subject_data.get('subject6')
                    subject7 = subject_data.get('language')
                d=studentmark1.objects.filter(s1__s__email=email)
                for obj in d:
                    obj.subject1 = s1
                    obj.subject2 = s2
                    obj.subject3 = s3
                    obj.subject4 = s4
                    obj.subject5 = s5
                    obj.subject6 = s6
                    obj.languages =s7
                    obj.save()
                    mark = f"Second internal marks:{subject1} : {s1}, {subject2} : {s2}, {subject3} : {s3}, {subject4} : {s4}, {subject5} : {s5}, {subject6} : {s6}, {subject7} : {s7}"
                    subjects='I internal marks updated mark'
                    message=f'{mark}'
                    email_from= settings.EMAIL_HOST_USER
                    recipeient_list=[email]
                    send_mail(subjects,message,email_from,recipeient_list) 
                classes=classes
                course=course
                internal=internal
                url = reverse('updatemore') + f"?classes={classes}&course={course}&internal={internal}"
                context = {
                    "message": "Marks saved successfully.If you want to send marks in email click open url",
                    "url": url
                }
                return render(request, "messegelink.html", context)
            elif internal=="II Internal":
                d=studentmark2.objects.filter(s1__s__email=email)
                for obj in d:
                    obj.subject1 = s1
                    obj.subject2 = s2
                    obj.subject3 = s3
                    obj.subject4 = s4
                    obj.subject5 = s5
                    obj.subject6 = s6
                    obj.languages =s7
                    obj.save()
                classes=classes
                course=course
                internal=internal
                url = reverse('updatemore') + f"?classes={classes}&course={course}&internal={internal}"
                context = {
                    "message": "Marks saved successfully.If you want to send marks in email click open url",
                    "url": url
                }
                return render(request, "messegelink.html", context)
       
def backtomy_form(request):
    return render(request,'my_form.html')

def backtostudentrights(request):
    return render(request,"studentrights.html")

def editlecturerprofile(request):
    if request.method=="POST":
        btn=request.POST.get("btn"," ")
        if "ledit" in btn:
            name=request.POST.get("lname")
            nimage = request.FILES.get('nimage')
            cls=request.POST.get("lclass")
            cour=request.POST.get("lcourse")
            nemail=request.POST.get("lemail")
            oldemail=request.POST.get("oldlemail")
            le=lecturer.objects.get(le__email=oldemail)
            if le is not None:
                le.classes=cls
                le.course=cour
                le.le.email=nemail
                le.le.first_name=name
                if nimage is not None:
                    le.image=nimage
                le.save()
                le.le.save()
                return redirect(lecturer_edit,course=le.course,type="is_lecturer")
        elif 'sedit' in btn:
            sname=request.POST.get('sname')
            simage = request.FILES.get('simage')
            oldemail=request.POST.get('oldemail')
            semail=request.POST.get('semail')
            oldemail=request.POST.get('oldemail')
            st=staff.objects.get(st__email=oldemail)
            if st is not None:
                st.st.email=semail
                st.st.first_name=sname
                if simage is not None:
                    st.image=simage
                st.save()
                st.st.save()
                email1=st.st.email
                print("hello")
                users=User.objects.filter(email=email1).first()
                if users.is_staff==True:
                    return redirect(staff_edit11,type="is_staff")
                elif users.is_librarian==True:
                    return redirect(staff_edit11,type="is_librarian")
                elif users.is_princi==True:
                    return redirect(staff_edit11,type="is_princi")
                elif users.is_clerk==True:
                    return redirect(staff_edit11,type="is_clerk")

def studentedit(request, course=None,classes=None):
        students = student.objects.filter(s__is_student=True,course=course,classes=classes)
        context = {
            'students': students,
        }
        return render(request, 'studentedit.html',context)
def studentedit2(request, course=None,classes=None):
        students = student.objects.filter(s__is_student=True,course=course,classes=classes)
        context = {
            'students': students,
        }
        return render(request, 'studenteditprinci.html',context)
def studentedit1(request):
    if request.method=="POST":
            name=request.POST.get("sname")
            nimage = request.FILES.get('nimage')
            cls=request.POST.get("sclass")
            cour=request.POST.get("scourse")
            nemail=request.POST.get("semail")
            oldemail=request.POST.get("oldsemail")
            s=student.objects.get(s__email=oldemail)
            if s is not None:
                s.classes=cls
                s.course=cour
                s.s.email=nemail
                s.s.first_name=name
                if nimage is not None:
                    s.image=nimage
                s.save()
                s.s.save()
                return redirect(studentedit,course=s.course,classes=s.classes)    

def studentedit12(request):
    if request.method=="POST":
            name=request.POST.get("sname")
            nimage = request.FILES.get('nimage')
            cls=request.POST.get("sclass")
            cour=request.POST.get("scourse")
            nemail=request.POST.get("semail")
            oldemail=request.POST.get("oldsemail")
            s=student.objects.get(s__email=oldemail)
            if s is not None:
                s.classes=cls
                s.course=cour
                s.s.email=nemail
                s.s.first_name=name
                if nimage is not None:
                    s.image=nimage
                s.save()
                s.s.save()
                return redirect(studentedit2,course=s.course,classes=s.classes)        
def editlecturerprofile1(request):
    if request.method=="POST":
        btn=request.POST.get("btn"," ")
        if "ledit" in btn:
            name=request.POST.get("lname")
            nimage = request.FILES.get('nimage')
            cls=request.POST.get("lclass")
            cour=request.POST.get("lcourse")
            nemail=request.POST.get("lemail")
            oldemail=request.POST.get("oldlemail")
            le=lecturer.objects.get(le__email=oldemail)
            if le is not None:
                le.classes=cls
                le.course=cour
                le.le.email=nemail
                le.le.first_name=name
                if nimage is not None:
                    le.image=nimage
                le.save()
                le.le.save()
                return redirect(lecturer_edit1,course=le.course,type="is_lecturer")
        elif 'sedit' in btn:
            sname=request.POST.get('sname')
            simage = request.FILES.get('simage')
            oldemail=request.POST.get('oldemail')
            semail=request.POST.get('semail')
            oldemail=request.POST.get('oldemail')
            st=staff.objects.get(st__email=oldemail)
            if st is not None:
                st.st.email=semail
                st.st.first_name=sname
                if simage is not None:
                    st.image=simage
                else:
                    st.save()
                    st.st.save()
                st.save()
                st.st.save()
                email1=st.st.email
                print("hello")
                users=User.objects.filter(email=email1).first()
                if users.is_staff==True:
                    return redirect(staff_edit1,type="is_staff")
                elif users.is_librarian==True:
                    return redirect(staff_edit1,type="is_librarian")
                elif users.is_princi==True:
                    return redirect(staff_edit1,type="is_princi")
                elif users.is_clerk==True:
                    return redirect(staff_edit1,type="is_clerk")
            
def lecturer_edit1(request, course=None,type=None):
    if 'is_lecturer' in type:
        lecturerinfo_bca = lecturer.objects.filter(le__is_lecturer=True,course=course)
        context = {
            'lecturerinfo_bca': lecturerinfo_bca,
        }
        return render(request, 'editlectureprofile1.html',context)
def staff_edit1(request,type=None):
    if 'is_staff' in type:
        staffview = staff.objects.filter(st__is_staff=True)
        context = {
                'staffsview': staffview,
                    }
        return render(request, 'editstaffprofile1.html',context)
    if 'is_clerk' in type:
        staffview = staff.objects.filter(st__is_clerk=True)
        context = {
                'staffsview': staffview,
                    }
        return render(request, 'editstaffprofile1.html',context)
    if 'is_librarian' in type:
        staffview = staff.objects.filter(st__is_librarian=True)
        context = {
                'staffsview': staffview,
                    }
        return render(request, 'editstaffprofile1.html',context)
    if 'is_princi' in type:
        staffview = staff.objects.filter(st__is_princi=True)
        context = {
                'staffsview': staffview,
                    }
        return render(request, 'editstaffprofile1.html',context)
    
def staff_edit11(request,type=None):
    if 'is_staff' in type:
        staffview = staff.objects.filter(st__is_staff=True)
        context = {
                'staffsview': staffview,
                    }
        return render(request, 'editstaffprofile.html',context)
    if 'is_clerk' in type:
        staffview = staff.objects.filter(st__is_clerk=True)
        context = {
                'staffsview': staffview,
                    }
        return render(request, 'editstaffprofile.html',context)
    if 'is_librarian' in type:
        staffview = staff.objects.filter(st__is_librarian=True)
        context = {
                'staffsview': staffview,
                    }
        return render(request, 'editstaffprofile.html',context)
    if 'is_princi' in type:
        staffview = staff.objects.filter(st__is_princi=True)
        context = {
                'staffsview': staffview,
                    }
        return render(request, 'editstaffprofile.html',context)
    
def lecturer_edit(request, course=None,type=None):
    if 'is_lecturer' in type:
        lecturerinfo_bca = lecturer.objects.filter(le__is_lecturer=True,course=course)
        context = {
            'lecturerinfo_bca': lecturerinfo_bca,
        }
        return render(request, 'editlectureprofile.html',context)
    
def register1(request):
    return render(request,"register.html")   

def register(request):
    if request.method=="POST":
        email=request.POST.get("email")
        email1=appliedinfo.objects.filter(email_id=email).first()
        if email1 is None:
            otp = ''.join([str(random.randint(0, 9)) for _ in range(6)])
            subject='OTP for application'
            message=f'Hi ,your otp is {otp}'
            email_from= settings.EMAIL_HOST_USER
            recipeient_list=[email]
            send_mail(subject,message,email_from,recipeient_list)
            messages.success(request,"Email sent")
            return render(request, 'otp1.html', {'otp': otp})
        else:
            messages.success(request,"You already applied..:)")
            return render(request,"register.html")
        
def checkotp1(request):
    if request.method=="POST":
        gotp=request.POST.get("gotp")
        otp = request.POST.get("otp")
        if otp==gotp:
            return render(request,"application.html")
        else:
            messages.success(request,"OTP does not match..?")
            return render(request,'otp1.html')

def application(request):
    if request.method=="POST":
        fname=request.POST.get('name')
        lname=request.POST.get('lname')
        cno=request.POST.get('tel')
        emailid=request.POST.get('email')
        gender=request.POST.get('gender')
        aadhar=request.POST.get('aadhar')
        dob=request.POST.get('dob')
        place_of_birth=request.POST.get('placeofbirth')
        caste=request.POST.get('caste')
        category=request.POST.get('category')
        parentsname=request.POST.get('parentsname')
        occupation=request.POST.get('occupation')
        parentsno=request.POST.get('parentsno')
        income=request.POST.get('income')
        address=request.POST.get('address')
        course=request.POST.get('course')
        language=request.POST.get('language')
        regno=request.POST.get('regno')
        daob=datetime.strptime(dob,'%Y-%m-%d').date()
        current_date=datetime.today().date()
        age=current_date.year-daob.year-((current_date.month,current_date.day)<(daob.month,daob.day))
        if age>=17 and age<=19:
            my_user=appliedinfo(name=fname,lastname=lname,contact_no=cno,email_id=emailid,gender=gender,adharno=aadhar,dob=dob,place_of_birth=place_of_birth,caste=caste,category=category, parents_name=parentsname,occupation=occupation,parent_no=parentsno,income=income,address=address,course=course,language=language,regno=regno)
            my_user.save()
            return redirect("pay")
        else:
            messages.success(request,"Age must be inbetween 17 and 19")
            return render(request,'application.html')
    else:
        return render(request,'application.html')
    
    
    
def pay(request):
    if request.method=="POST":
        rs=request.POST.get('rs')
        fee=int(rs)
        if fee==100:
            my_user=appliedinfo.objects.all()
            my_user.update(pay=rs)
            messages.success(request,f"You paid{rs} and your successfully registered")
            return render(request,"home.html")
        else:
            messages.success(request,"Please pay 100 rupees")
    return render(request,'pay.html')
    
# def displayappinfo(request):
#     user=appliedinfo.objects.filter(pay=" ")
#     user.delete()
#     applist=appliedinfo.objects.filter(pay="100")
#     return render(request,'displayappinfo.html',{'applist':applist})
def appinfo(request):
    user=appliedinfo.objects.filter(pay=" ")
    user.delete()
    applist=appliedinfo.objects.filter(pay="100")
    return render(request,'appinfo.html',{'applist':applist})

def libhome(request):
    if request.user.is_anonymous:
        messages.success(request,"your a not login...please login")
        return render(request,"plogin.html")
    return render(request,'libhome.html')

def ulibback(request):
    if request.user.is_anonymous:
        messages.success(request,"your a not login...please login")
        return render(request,"plogin.html")
    return render(request,'ulib.html')

def removebook(request,id=None):
    book=bookdetails.objects.filter(bookid=id)
    if book is not None: 
        book.delete()
        type="Novel"
        url = reverse('messagelib') + f"?type={type}"
        context = {
        "message": "Book deleted",
        "url": url
        }
        return render(request, "messegelink.html", context) 
def addbook(request):
    if True:
        id = 1 if bookdetails.objects.count() == 0 else int(bookdetails.objects.aggregate(max=Max('bookid'))["max"]) + 1
        context = {'id':id}
        if request.method=="POST":
            image=request.FILES['image']
            bookname=request.POST.get('bookname')
            author=request.POST.get('author')
            copies=request.POST.get('copies')
            pub=request.POST.get('publication')
            type=request.POST.get('booktype')
            book=bookdetails.objects.filter(bookname=bookname).first()
            if book is not None:
                messages.success(request,"Book already exists")
                return render(request,'addbook.html')
            else:
                my_user=bookdetails(bookid=id,bookimg=image,bookname=bookname,author=author,copies=copies,total_copies=copies,publication=pub,type=type)
                my_user.save()
                messages.success(request,"Inserted")
                return render(request,"addbook.html")
        return render(request, 'addbook.html', context) 

def messagelib(request):
    type = request.GET.get('type')
    books=bookdetails.objects.filter(type=type)
    context={'books':books}
    return render(request,'libbookissue.html',context)

def returnbook(request):
    if request.method=="POST":
        bookid=request.POST.get('id')
        bookname=request.POST.get('bookname')
        book=bookdetails.objects.filter(bookid=bookid,bookname=bookname,status="Issued").first()
        if book is not None and book.status=="Issued":
            book.status="Available"
            book.save()
            messages.success(request,"Returned")
        else:
            messages.success(request,"Book already returned")
    return render(request,'returnbook.html')

def book_view(request,type=None):
    books=bookdetails.objects.filter(type=type)
    context={'books':books}
    return render(request,'bookview.html',context)

def aboutlib(request,type=None):
    books=bookdetails.objects.filter(type=type)
    context={'books':books}
    return render(request,'about.html',context)
def aboutlib1(request,type=None):
    books=bookdetails.objects.filter(type=type)
    context={'books':books}
    return render(request,'aboutbook.html',context)
def aboutlib2(request,type=None):
    books=bookdetails.objects.filter(type=type)
    context={'books':books}
    return render(request,'aboutbook11.html',context)
def libbook_view(request,type=None):
    books=bookdetails.objects.filter(type=type)
    context={'books':books}
    return render(request,'libbookissue.html',context)

def myview1(request):
    k=request.POST.get('btn',"")
    if "b1" in k:
        if request.method == 'POST':
            bookid = request.POST.get('bookid')
            email=request.POST.get('email')
            u=User.objects.filter(email=email).first()
            if u is None:
                type="Novel"
                url = reverse('messagelib') + f"?type={type}"
                context = {
                        "message": "Not a valid email",
                        "url": url
                    }
                return render(request, "messegelink.html", context) 
            else:
                book = bookdetails.objects.get(bookid=bookid)
                type=book.type
                count=book.copies
                if count==0:
                    url = reverse('messagelib') + f"?type={type}"
                    context = {
                        "message": "Book not available all are issued",
                        "url": url
                    }
                    return render(request, "messegelink.html", context) 
                elif book.status == 'Available' and book.copies == 1:
                    count = count - 1
                    book.copies = count
                    book.status = 'Issued'
                    borrower_list = book.borrower.split(',') if book.borrower else []
                    borrower_list.append(email)
                    book.borrower = ','.join(borrower_list)
                    book.save()
                    print("Updated borrower list:", borrower_list)
                    type=book.type
                    url = reverse('messagelib') + f"?type={type}"
                    context = {
                        "message": "Book Issued.If you want to issue more books click open url",
                        "url": url
                    }
                    return render(request, "messegelink.html", context)     
                elif book.status == 'Available' and book.copies!=0:
                    count=count-1
                    book.copies=count
                    borrower_list = book.borrower.split(',') if book.borrower else []
                    borrower_list.append(email)
                    book.borrower = ','.join(borrower_list)
                    book.save()
                    booklist=bookdetails.objects.all()  
                    type=book.type                  
                    url = reverse('messagelib') + f"?type={type}"
                    context = {
                        "message": "Book Issued.If you want to issue more books click open url",
                        "url": url
                    }
                    return render(request, "messegelink.html", context)
    elif 'b2' in k: 
        if request.method == 'POST':
            bookid = request.POST.get('bookid')
            email1 = request.POST.get('email')
            u=User.objects.filter(email=email1).first()
            if u is None:
                type="Novel"
                url = reverse('messagelib') + f"?type={type}"
                context = {
                        "message": "Not a valid email",
                        "url": url
                    }
                return render(request, "messegelink.html", context) 
            book = bookdetails.objects.get(bookid=bookid)
            type = book.type
            count = book.copies
            borrower = book.borrower
            borrower_list = borrower.split(',') if borrower else []
            if email1 not in borrower_list:
                type="Novel"
                url = reverse('messagelib') + f"?type={type}"
                context = {
                        "message": "Email not found in borrower list",
                        "url": url
                    }
                return render(request, "messegelink.html", context)
            elif book.status == 'Available' and book.copies==book.total_copies :                
                url = reverse('messagelib') + f"?type={type}"
                context = {
                    "message": "No Book issued",
                    "url": url
                }
                return render(request, "messegelink.html", context) 
            elif book.status == 'Available' and book.copies!=0:
                count=count+1
                book.copies=count
                borrower_list.remove(email1)
                borrower = ','.join(borrower_list)
                book.borrower = borrower
                book.save()
                type=book.type
                url = reverse('messagelib') + f"?type={type}"
                context = {
                    "message": "Book returned.If you want to return more books click open url",
                    "url": url
                }
                return render(request, "messegelink.html", context)    
            elif book.status == 'Issued' and book.copies==0:
                count=count+1
                book.copies=count
                book.status = 'Available'
                borrower_list.remove(email1)
                borrower = ','.join(borrower_list)
                book.borrower = borrower
                book.save()
                booklist=bookdetails.objects.all()
                type=book.type
                url = reverse('messagelib') + f"?type={type}"
                context = {
                    "message": "Book returned.If you want to return more books click open url",
                    "url": url
                }
                return render(request, "messegelink.html", context)         
        return render(request, 'libbookissue.html', {'booklist': booklist})  
    
def libbookissue(request):
    booklist=bookdetails.objects.all()
    context={'issuelist':booklist}
    return render(request,'libbookissue.html',context) 

def aboutbook(request):
    books = bookdetails.objects.all()
    return render(request, 'aboutbook.html', {'about': books})

def ulibhome(request):
    return render(request,'ulib.html')

def book_view(request,type=None):
    books=bookdetails.objects.filter(type=type)
    context={'books':books}
    return render(request,'bookview.html',context)

def issueview(request):
    issuelist=bookdetails.objects.filter(status="Issued")
    context={'issuelist':issuelist}
    return render(request,'issueview.html',context)  

def bookview(request):
    booklist=bookdetails.objects.all()
    context={'issuelist':booklist}
    return render(request,'bookview.html',context) 

def returnview(request):
    Availablelist=bookdetails.objects.filter(status="Available")
    return render(request,'returnview.html',{'Availablelist':Availablelist}) 

def booklist(request):
    books = bookdetails.objects.all()
    return render(request, 'booklist.html', {'booklist': books})

def issue_book(request):
    k=request.POST.get('btn',"")
    if "b1" in k:
        if request.method == 'POST':
            bookid = request.POST.get('bookid')
            try:
                book = bookdetails.objects.get(bookid=bookid)
                count=book.copies
                if count==0:
                    messages.success(request,"Books not available ,All are issued")
                    return render(request,'bookview.html')
                elif book.status == 'Available' and book.copies==1 :
                    count=count-1
                    book.copies=count
                    book.status = 'Issued'
                    logged_in_user = request.user
                    email = logged_in_user.email
                    borrower_list = book.borrower.split(',') if book.borrower else []
                    borrower_list.append(email)
                    book.borrower = ','.join(borrower_list)
                    book.save()
                    type1=book.type
                    messages.success(request, "Book issued")
                    return redirect('book_view',type=type1)    
                elif book.status == 'Available' and book.copies!=0:
                    count=count-1
                    book.copies=count
                    logged_in_user = request.user
                    email = logged_in_user.email
                    borrower_list = book.borrower.split(',') if book.borrower else []
                    borrower_list.append(email)
                    book.borrower = ','.join(borrower_list)
                    book.save()
                    type1=book.type
                    messages.success(request, "Book issued")
                    return redirect('book_view',type=type1)
                else:    
                    messages.success(request, "Book is already issued")
                    return render(request, 'bookview.html')
            except bookdetails.DoesNotExist:
                messages.error(request, "Book not found")
    return redirect('book_view',type=type1)

def about1(request):
    booklist=bookdetails.objects.all()
    context={'issuelist':booklist}
    return render(request,'about.html',context)  

def book_search(request):
    query = request.GET.get('q')
    if query:
        books = bookdetails.objects.filter(title__istartswith=query)
    else:
        books = []
    return render(request, 'book_search.html', {'books': books, 'query': query})

def autocomplete(request):
    query = request.GET.get('q', '')
    results = []
    if query:
        books = bookdetails.objects.filter(bookname__icontains=query)
        results = [book.bookname for book in books]
    return JsonResponse(results, safe=False)

def search(request):
    query = request.GET.get('q', '')
    results = []
    if query:
        books = bookdetails.objects.filter(bookid=query) | bookdetails.objects.filter(bookname__icontains=query)
        results = [{
            'bookid': book.bookid,
            'bookname': book.bookname,
            'author': book.author,
            'borrower': book.borrower
        } for book in books]
    return JsonResponse(results, safe=False)

def backtocanteen(request):
    return render(request,"canteen.html")
def backtolibrary(request):
    return render(request,"finallibrary.html")



    

        
     
