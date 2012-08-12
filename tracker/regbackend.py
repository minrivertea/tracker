from django.conf import settings
from django.contrib.sites.models import RequestSite
from django.contrib.sites.models import Site
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from registration import signals
from registration.models import RegistrationProfile
from django.contrib import messages


attrs_dict = {'class': 'required'}



class CustomBackend(object):

    def register(self, request, **kwargs):
                
        username, email, password = kwargs['email'], kwargs['email'], kwargs['password1']
        if Site._meta.installed:
            site = Site.objects.get_current()
        else:
            site = RequestSite(request)
        new_user = RegistrationProfile.objects.create_inactive_user(username, email,
                                                                    password, site)
        
        # we'll secretly log the user in now
        from django.contrib.auth import load_backend, login
        for backend in settings.AUTHENTICATION_BACKENDS:
            if new_user == load_backend(backend).get_user(new_user.pk):
                new_user.backend = backend
        if hasattr(new_user, 'backend'):
            login(request, new_user)
        
        signals.user_registered.send(sender=self.__class__,
                                     user=new_user,
                                     request=request)
        
        
        text = "We've sent you a verification email - please check it now!"
        messages.warning(request, text)
                                
        return new_user


    def registration_allowed(self, request):
        return getattr(settings, 'REGISTRATION_OPEN', True)

    def get_form_class(self, request):
        return CustomRegistrationForm

    def post_registration_redirect(self, request, user):
        return ('home', (), {})
        # return ('registration_complete', (), {})

    def post_activation_redirect(self, request, user):
        return ('registration_activation_complete', (), {})




class CustomRegistrationForm(forms.Form):
    """
    Form for registering a new user account.
    
    Validates that the requested username is not already in use, and
    requires the password to be entered twice to catch typos.
    
    Subclasses should feel free to add any additional validation they
    need, but should avoid defining a ``save()`` method -- the actual
    saving of collected user data is delegated to the active
    registration backend.
    
    """

    email = forms.EmailField(widget=forms.TextInput(attrs=dict(attrs_dict,
                                                               maxlength=75)),
                             label=_("Email"))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict, render_value=False),
                                label=_("Password"))
    
    def clean_email(self):
        """
        Validate that the email is not already in use.
        
        """
        existing = User.objects.filter(email__iexact=self.cleaned_data['email'])
        if existing.exists():
            raise forms.ValidationError(_("A user with that email address already exists."))
        else:
            return self.cleaned_data['email']

