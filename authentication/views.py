from .models import User
from .forms import ( 
    UserRegistrationForm,
    UserLoginForm,
    SendResetPasswordEmailForm,
    ResetPasswordForm,
    UserProfileForm 
    )


from django.views import View
from django.views.generic import FormView,CreateView,DetailView,UpdateView


from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.core.exceptions import ValidationError


from django.contrib import messages
from django.contrib.auth import authenticate,login as auth_login , logout,update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm 
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import PasswordResetTokenGenerator


from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import smart_str




class UserRegistrationView(CreateView):
    model=User
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
    
class UserLogoutView(View,LoginRequiredMixin):
    template_name = 'authentication/logout.html'
    login_url = 'login'

    def post(self, request):
        logout(request)
        return redirect(self.login_url)

    def get(self, request):
        return render(request, self.template_name)



class ChangePasswordView(View,LoginRequiredMixin):
    template_name='authentication/change_password.html'

    def post(self, request):
        form=PasswordChangeForm(request.user,request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request,form.user)
            messages.success(request, 'Your password has been changed successfully.')
            return redirect('/')
        else:
            messages.error(request, 'Please correct the error below.')
            context={'form':form}
            return render(request,self.template_name,context)

    def get(self, request):
        form=PasswordChangeForm(request.user)
        return render(request, self.template_name,{'form':form})
    

    def dispatch(self, request, *args ,**kwargs) :
        if request.user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect('login')
        

class SendResetPasswordEmailView(View):
    template_name = 'authentication/send_reset_password_email.html'  

    def get(self, request):
        form = SendResetPasswordEmailForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = SendResetPasswordEmailForm(request.POST)
        if form.is_valid():
            return render(request,'authentication/email_sent.html')
        else:
            messages.error(request,"User doesn't exist with the given email")
            return render(request,self.template_name,{'form':form})
        
    def dispatch(self, request, *args ,**kwargs) :
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return super().dispatch(request, *args, **kwargs)

class PasswordResetView(View):
    template_name='authentication/password_reset.html'

    def get(self,request,uid=None, token=None):
        form =ResetPasswordForm()
        return render(request, self.template_name, {'form': form})

    def post(self,request,uid,token):
        form =ResetPasswordForm(request.POST)
        if form.is_valid():
            user_id=smart_str(urlsafe_base64_decode(uid))

            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                raise ValidationError("User not found")
        
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise ValidationError("Token Expired or Invalid")

            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('login')
        
        return render(request, self.template_name, {'form': form})

    def dispatch(self, request, *args ,**kwargs) :
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return super().dispatch(request, *args, **kwargs)
        


class UserProfileView(DetailView):
    model = User
    template_name = 'authentication/user_profile.html'
    context_object_name = 'user'


class UpdateProfileView(UpdateView,LoginRequiredMixin):
    form_class=UserProfileForm
    model=User
    template_name='authentication/update_profile.html'

    def get_object(self) :
        return self.request.user 
    
    def get_success_url(self) -> str:
        return reverse('user-profile',args=[self.request.user.pk])