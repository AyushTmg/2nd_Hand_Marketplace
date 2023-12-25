from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import FormView
from .forms import UserRegistrationForm,UserLoginForm
from django.contrib.auth import authenticate,login as auth_login , logout
from django.urls import reverse_lazy
from django.contrib import messages


class UserRegistrationView(FormView):
    template_name='authentication/registration.html'
    form_class=UserRegistrationForm
    success_url=reverse_lazy("login")
    
    def dispatch(self, request ,*args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('/')
        return super().dispatch(request,*args,**kwargs)
    
class UserLoginView(FormView):
    template_name='authentication/login.html'
    form_class=UserLoginForm
    success_url="/"
    # success_url=reverse_lazy("/")

    def form_valid(self, form):
        email=form.cleaned_data['email']
        password=form.cleaned_data['password']
        user=authenticate(email=email,password=password)
        if user is not None:
            auth_login(self.request,user)
            return super().form_valid(form)
        else:
             form.add_error(None,'Invalid Login Credintals') 
             return self.form_invalid(form)


    def dispatch(self, request ,*args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('/')
        return super().dispatch(request,*args,**kwargs)
    
class UserLogoutView(View):
    template_name = 'authentication/logout.html'
    login_url = 'login'

    def post(self, request):
        logout(request)
        return redirect(self.login_url)

    def get(self, request):
        return render(request, self.template_name)
    
    def dispatch(self, request, *args,**kwargs) :
        if request.user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)
        return redirect(self.login_url)




