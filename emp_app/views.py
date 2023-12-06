from django.shortcuts import render, HttpResponse, redirect
from .models import Employee, Role, Department, Client, Project
from datetime import datetime
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders



@login_required(login_url='login')
def signUpPage(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')

        if pass1 != pass2:
            return HttpResponse("Your password and confirm password are not Same!!")
        else:
            my_user = User.objects.create_user(uname, email, pass1)
            my_user.save()
            return redirect('login')

    return render(request, 'employees/signup.html')

def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        pass1 = request.POST.get('pass')
        user = authenticate(request, username=username, password=pass1)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return HttpResponse("Username or Password is incorrect!!!")

    return render(request, 'employees/login.html')


def logoutPage(request):
	logout(request)
	return redirect('login')
    

def dashboard(request):
    projects = Project.objects.all()
    context = {
        'projects': projects
    }
    return render(request, 'employees/dashboard.html',context)


def all_emp(request):
    emps = Employee.objects.all()
    context = {
        'emps': emps
    }
    return render(request, 'employees/view_all_emp.html', context)
    
def add_emp(request):
    depts = Department.objects.all()
    roles = Role.objects.all()
   
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        dept = request.POST.get('dept')
        role = request.POST.get('role')
        dept_instance = Department.objects.get(name=dept)
        role_instance = Role.objects.get(name=role)
        salary = request.POST.get('salary')
        bonus = request.POST.get('bonus')
        hire_date = request.POST.get('hire_date')

        Employee.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            dept = dept_instance,
            role= role_instance,
            salary=salary,
            bonus=bonus,
            hire_date=hire_date,
        )
    context = {
         "depts": depts,
         "roles": roles,
        } 
    return render(request, 'employees/add_emp.html',context)
    
def remove_emp(request, emp_id=0):
    if emp_id:
        try:
            emp_to_be_removed = Employee.objects.get(id=emp_id)
            emp_to_be_removed.delete()
            return HttpResponse("Employee Removed Successfully")
            # return render(request, 'remove_emp.html')
        except:
            return HttpResponse("Please Enter A Valid EMP ID")
    emps = Employee.objects.all()
    context = {
        'emps': emps
    }
    return render(request, 'employees/remove_emp.html', context)

def filter_emp(request):
    if request.method == 'POST':
        name = request.POST['name']
        dept = request.POST['dept']
        role = request.POST['role']
        emps = Employee.objects.all()

        if name:
            emps = emps.filter(Q(first_name__icontains=name)
                               | Q(last_name__icontains=name))
        if dept:
            emps = emps.filter(dept__name__icontains=dept)
        if role:
            emps = emps.filter(role__name__icontains=role)

        context = {
            'emps': emps
        }
        return render(request, 'employees/view_all_emp.html', context)

    elif request.method == 'GET':
        return render(request, 'employees/filter_emp.html')
    else:
        return HttpResponse('An Exception Occured')

def edit_emp(request,emp_id=0):
    
    emp = Employee.objects.get(id=emp_id)
    
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        
        emp.first_name=first_name
        emp.last_name=last_name
        emp.email=email
        emp.phone=phone
    
        emp.save()
        return redirect('all_emp')
    context = {
        'emp': emp,  
    }
    return render(request, 'employees/edit_emp.html', context)

def emp_details(request,emp_id=0):
    emp = Employee.objects.get(id=emp_id)
    context = {
        'emp': emp,
    }
    return render(request,'employees/emp_details.html',context)

def payslip(request, emp_id):
    emp = Employee.objects.get(id=emp_id)
    template_path = 'payroll/payslip.html'
    context = {
        'emp': emp,
    }
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

def employee_list(request):
    emps = Employee.objects.all()
    context = {
        'emps': emps
    }
    return render(request, 'payroll/employee_list.html', context)

def index(request):
    return render(request, 'employees/index.html')

def all_client(request):
    clients = Client.objects.all()
    context = {
        'clients': clients
    }
    return render(request, 'clients/all_client.html', context)

def add_client(request):
    
    clients = Client.objects.all()
    
    if request.method == 'POST':
        client_name = request.POST.get('client_name')
        client_email = request.POST.get('client_email')
        client_phone = request.POST.get('client_phone')
        gender = request.POST.get('gender')
        website = request.POST.get('website')
                                  
        Client.objects.create(
            client_name=client_name,
            client_email=client_email,
            client_phone=client_phone,
            gender=gender,
            website = website,
        )
        
    context= {
        "clients": clients
    } 
    return render(request, 'clients/add_client.html', context=context)

def remove_client(request, client_id=0):
    if client_id:
        try:
            client_to_be_removed = Client.objects.get(id=client_id)
            client_to_be_removed.delete()
            return HttpResponse("Client Removed Successfully")
        except:
            return HttpResponse("Please Enter A Valid Client ID")
    clients = Client.objects.all()
    context = {
        'clients': clients
    }
    return render(request, 'clients/remove_client.html', context=context)

def all_project(request):
    projects = Project.objects.all()
    context = {
        'projects': projects
    }
    return render(request, 'projects/all_project.html', context)

def add_project(request):
    clients = Client.objects.all()
    
    if request.method == 'POST':
        project_name = request.POST.get('project_name')
        client_name = request.POST.get('client_name')
        project_details = request.POST.get('project_details')
        amount = request.POST.get('amount')
        priority = request.POST.get('priority')
        client_instance = Client.objects.get(client_name=client_name)
                                  
        Project.objects.create(
            project_name=project_name,
            client_name=client_instance,
            project_details=project_details,
            amount=amount,
            priority=priority,
        )
        
    context= {
        
        "clients": clients,
    } 
    return render(request, 'projects/add_project.html', context=context)  
    
def remove_project(request, project_id=0):
    if project_id:
        try:
            project_to_be_removed = Client.objects.get(id=project_id)
            project_to_be_removed.delete()
            return HttpResponse("Project Removed Successfully")
        except:
            return HttpResponse("Please Enter A Valid Project ID")
    projects = Project.objects.all()
    context = {
        'projects': projects
    }
    return render(request, 'projects/remove_project.html', context=context)