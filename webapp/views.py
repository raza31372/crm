from django.shortcuts import render, redirect
from .forms import CreateUserForm, LoginForm, CreateRecordForm, UpdateRecordForm

from django.contrib.auth.models import auth
from django.contrib.auth import authenticate

from django.contrib.auth.decorators import login_required

from .models import Record

from django.contrib import messages



def home(request):

    # return HttpResponse('Hello World')
    context = {'page': 'Home'}

    return render(request, 'webapp/index.html',context)



def register(request):

    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        
        if form.is_valid():
            form.save()

            messages.success(request, 'Account created successfully')

            return redirect("my-login")
    
    context = {'form':form, 'page':'Register'}

    return render(request, 'webapp/register.html', context=context)



def my_login(request):

    form = LoginForm()  #from forms.py class LoginForm()

    if request.method == "POST":
        form = LoginForm(request, data=request.POST)

        if form.is_valid():
            username = request.POST.get('username')    
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                auth.login(request, user)
                
                return redirect("dashboard")

    context = {'form':form, 'page':'Login'}

    return render(request, 'webapp/my-login.html', context=context)



@login_required(login_url='my-login')
def dashboard(request):

    my_records = Record.objects.all()

    context = {'records': my_records ,'page': 'Dashboard'}

    return render(request, 'webapp/dashboard.html', context=context)



# Create a record

@login_required(login_url='my-login')
def create_record(request):

    form = CreateRecordForm()

    if request.method == "POST":
         form = CreateRecordForm(request.POST)

         if form.is_valid():
             form.save()

             messages.success(request, 'Record created successfully')

             return redirect("dashboard")
    
    context = {'form':form, 'page':'Create Record'}

    return render(request, 'webapp/create-record.html', context=context)



# Update a record

@login_required(login_url='my-login')
def update_record(request, pk):

    record = Record.objects.get(id=pk)
    form = UpdateRecordForm(instance=record)

    if request.method == "POST":

        form = UpdateRecordForm(request.POST, instance=record)

        if form.is_valid():

            form.save()

            messages.success(request, 'Record Updated successfully')

            return redirect("dashboard")
        
    context = {'form':form, 'page':'Update Record'}

    return render(request, 'webapp/update-record.html', context=context)



# Read / View a person record

@login_required(login_url='my-login')
def view_record(request, pk):

    all_records = Record.objects.get(id=pk)

    context = {'records':all_records, 'page':'View Record'}

    return render(request, 'webapp/view-record.html', context=context)



@login_required(login_url='my-login')
def delete_record(request, pk):
    record = Record.objects.get(id=pk)
    record.delete()
    messages.success(request, 'Record Deleted successfully')
    return redirect("dashboard")

    

def user_logout(request):

    auth.logout(request)
    context = {'page':'Logout'}

    messages.success(request, 'Logout successfully')

    return redirect("my-login")





