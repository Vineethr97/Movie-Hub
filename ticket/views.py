from django.shortcuts import render,redirect
from django.views.generic import View,FormView,CreateView,TemplateView,ListView,DetailView,UpdateView
from ticket.forms import RegistrationForm,LoginForm,MovieForm,MovieChangeForm,PasswordResetForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from ticket.models import Movies
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy

def sign_required(fn): 
    def wrapper(request,*args,**kwargs):
        if not request.user.is_authenticated:
            messages.error(request,"you must login")
            return redirect("signin")
        return fn(request,*args,**kwargs)
    return wrapper
    



class SignUpView(CreateView):
    model=User
    template_name="register.html"
    form_class=RegistrationForm
    success_url=reverse_lazy("signin")
    def form_valid(self, form):
        messages.success(self.request,"account created successpully")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request,"faild to create account ")
        return super().form_invalid(form)

    # def get(self,request,*args,**kwargs):
    #     form=self.form_class
    #     return render(request,self.template_name,{"form":form})
    # def post(self,request,*args,**kwargs):
    #     form=self.form_class(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         messages.success(request,"account has been created")
    #         return redirect("signup")
    #     messages.error(request,"faild to register")
    #     return render(request,self.template_name,{"form":form})
    
class SignInView(View):
    model=User
    template_name="login.html"
    form_class=LoginForm

    def get(self,request,*args,**kwargs):
        form=self.form_class
        return render(request,self.template_name,{"form":form})
    def post(self,request,*args,**kwargs):
        form=self.form_class(request.POST)
        if form.is_valid():
            uname=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            usr=authenticate(request,username=uname,password=pwd)
            if usr:
                login(request,usr)
                messages.success(request,"login successfully")
                return redirect("index")
            messages.error(request,"invalid credentials")
            return render(request,self.template_name,{"form":form})
        
@method_decorator(sign_required,name="dispatch")
class IndexView(TemplateView):
    template_name="index.html"
    # def get(self,request,*args,**kwargs):
    #     return render(request,self.template_name)
    
@method_decorator(sign_required,name="dispatch")
class MovieCreateView(CreateView):
    model=Movies
    form_class=MovieForm
    template_name="movie-add.html"
    success_url=reverse_lazy("movie-list")

    def form_valid(self, form):
        form.instance.user=self.request.user
        messages.success(self.request,"")
        return super().form_valid(form)


    # def get(self,request,*args,**kwargs):
    #     form=self.form_class
    #     return render(request,self.template_name,{"form":form})
    # def post(self,request,*args,**kwargs):
    #     form=self.form_class(request.POST,files=request.FILES)
    #     if form.is_valid():
    #         form.save()
    #         messages.success(request,"movies added successfully")
    #         return redirect("movie-list")
    #     messages.error(request,"falid to add")
    #     return render(request,self.template_name,{"form":form})



@method_decorator(sign_required,name="dispatch")
class MovieListView(ListView):
    model=Movies
    template_name="movie-list.html"
    
    # context_object_name="movies"
    # def get_queryset(self):
    #     return Movies.objects.filter(user=self.request.user).order_by("id")
    
    def get(self,request,*args,**kwargs):
        qs=Movies.objects.all().order_by("id")
        return render(request,self.template_name,{"movies":qs})
    
@method_decorator(sign_required,name="dispatch")
class MovieDetailsView(DetailView):
    model=Movies
    template_name="movie-detail.html"
    context_object_name="movies"
    # def get(self,request,*args,**kwargs):
    #     id=kwargs.get("pk")
    #     qs=Movies.objects.get(id=id)
    #     return render(request,self.template_name,{"movies":qs})
    
@method_decorator(sign_required,name="dispatch")
class MovieEditView(UpdateView):
    model=Movies
    form_class=MovieChangeForm
    template_name="movie-edit.html"
    success_url=reverse_lazy("movie-list")


    # def get(self,request,*args,**kwargs):
    #     id=kwargs.get("pk")
    #     obj=Movies.objects.get(id=id)
    #     form=self.form_class(instance=obj)
    #     return render(request,self.template_name,{"form":form})
    # def post(self,request,*args,**kwargs):
    #     id=kwargs.get("pk")
    #     obj=Movies.objects.get(id=id)
    #     form=self.form_class(instance=obj,data=request.POST)
    #     if form.is_valid():
    #         form.save()
    #         messages.success(request,"movie changed")
    #         return redirect("movie-list")
    #     messages.error(request,"failed to update movie")
    #     return render(request,self.template_name,{"form":form})
    
@sign_required
def movie_delete_view(request,*args,**kwargs):
    id=kwargs.get("pk")
    Movies.objects.get(id=id).delete()
    messages.success(request,"movie removed")
    return redirect("movie-list")

def sign_out_view(request,*args,**kwargs):
    logout(request)
    messages.success(request,"logout")
    return redirect("signin")



class PasswordResetView(FormView):
    model=User
    template_name="password-reset.html"
    form_class=PasswordResetForm
    def post(self,request,*args,**kwargs):
        form=self.form_class(request.POST)

        if form.is_valid():
            username=form.cleaned_data.get("username")
            email=form.cleaned_data.get("email")
            pwd1=form.cleaned_data.get("password1")
            pwd2=form.cleaned_data.get("password2")

            if pwd1==pwd2:
                try:
                    usr=User.objects.get(username=username,email=email)
                    usr.set_password(pwd1)
                    usr.save()
                    messages.error(request,"password has been changed")
                    return redirect("signin")
                except Exception as e:
                    messages.error(request,"invalid credentials")
                    return render(request,self.template_name,{"form":form})
                else:
                    messages.error(request,"password mismatch")
                    return render(request,self.template_name,{"form":form})
                

                







