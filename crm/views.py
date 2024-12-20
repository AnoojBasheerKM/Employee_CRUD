from django.shortcuts import render,redirect,get_object_or_404

from django.views.generic import View

from crm.forms import EmployeeForm,SignUpForm,SignInform

from crm.models import Employee

from django.contrib.auth.models import User

from django.contrib.auth import authenticate,login,logout

from django.contrib import messages

from crm.decorators import signin_required

from django.contrib.auth.decorators import login_required

from django.utils.decorators import method_decorator

from django.views.decorators.cache import never_cache


# Create your views here.

decs=[signin_required,never_cache]

@method_decorator(decs,name="dispatch")
class EmployeeCreateView(View):
    
    template_name = "employeeadd.html"
    
    form_class = EmployeeForm
    
    def get(self,request,*args,**kwargs):
        
        form_instance = self.form_class()
        
        return render(request,self.template_name,{"form":form_instance})
    
    def post(self,request,*args,**Kwargs):
        
        form_data = request.POST
        
        form_instance = self.form_class(form_data,files=request.FILES)
        
        if form_instance.is_valid():
            
            form_instance.save()
            
            messages.success(request,"successfully added")
            
            return redirect("employee-add")
        
        messages.error(request,"failed to add")

        return render(request,self.template_name,{"form":form_instance})
 


@method_decorator(decs,name="dispatch")   
class EmployeeListView(View):
    
    template_name = "employee_list.html"
    
    def get(self,request,*args,**kwargs):
        
        qs = Employee.objects.all()
        
        return render(request,self.template_name,{"data":qs})

@method_decorator(decs,name="dispatch")
class EmployeeDeleteView(View):
    
    template_name = "employee_list.html"
    
    def get(self,request,*args,**kwargs):
        
        id = kwargs.get("pk")
        
        Employee.objects.get(id=id).delete()
        
        messages.success(request,"deleted successfully")
        
        return redirect("employee-list")
    
    
    
        
        

@method_decorator(decs,name="dispatch")
class EmployeeDetailView(View):
    
    template_name = "employee_details.html"
    
    def get(self,request,*args,**kwargs):
        
        id = kwargs.get("pk")

        qs = get_object_or_404(Employee,id=id)

        return render(request,self.template_name,{"data":qs})
    
    
@method_decorator(decs,name="dispatch")
class EmployeeEditView(View):

   template_name = "employee_edit.html"
   
   form_class = EmployeeForm
   
   def get(self,request,*args,**kwargs):
        
        id =kwargs.get("pk")

        empolyee_object = Employee.objects.get(id=id)

        form_instance = self.form_class(instance=empolyee_object) 

        return render(request,self.template_name,{"form":form_instance})
    
   def post(self,request,*args,**kwargs):
       
       id = kwargs.get("pk")
       
       employee_object = get_object_or_404(Employee,id=id)
       
       form_data = request.POST
       
       form_instance = self.form_class(form_data,files=request.FILES,instance=employee_object)
       
       if form_instance.is_valid():
           
           form_instance.save()
           
           messages.success(request,"updated successfully")
           
           return redirect("employee-list")
       
       messages.error(request,"updation failed")

       return render(request,self.template_name,{"form":form_instance})
   
class SignUpView(View):
    
    template_name = "signup.html"

    form_class = SignUpForm
    
    def get(self,request,*args,**kwargs):
        
        form_instance = self.form_class()

        return render(request,self.template_name,{"form":form_instance})
    
    def post(self,request,*args,**kwargs):
        
        form_data = request.POST
        
        form_instance = self.form_class(form_data)
        
        if form_instance.is_valid():
            
            data = form_instance.cleaned_data
            
            User.objects.create_user(**data)
            
            redirect("signin") 
            
        return render(request,self.template_name,{"form":form_instance}) 
    
class SignInView(View):
    
    template_name = "signin.html" 
    
    form_class = SignInform
    
    def get(self,request,*args,**kwargs):
        
        form_instance = self.form_class
        
        return render(request,self.template_name,{"form":form_instance})  
    
    def post(self,request,*args,**kwargs):
        
        form_data = request.POST
        
        form_instance = self.form_class(form_data)             

        if form_instance.is_valid():
            
            data = form_instance.cleaned_data
            
            uname = data.get("username")

            pwd = data.get("password")

            user_object = authenticate(request,username = uname,password = pwd)

            if user_object:
                
                login(request,user_object)
                
                return redirect("employee-list")
            
        return render(request,self.template_name,{"form":form_instance})


@method_decorator(decs,name="dispatch")
class SignOutView(View):
    
    def get(self,request,*args,**kwargs):
        
        logout(request)
        
        

        return redirect("signin")