from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


class LoginForm(forms.Form):
    """ LoginForm
    This form is used for the basic authentication for Django

    Form Members:
        - username : str --> the username passed from the login view
        - password : str --> the password passed from the login view
        - error_messages : dict --> Various error messages from the form
    
    Class Members:
        - request : dict --> dictionary given from View
        - user_cache : User --> User meta data used for this form instance

    Methods:
        + clean : dict --> returns a dict with the verified data
        + ConfirmLoginAllowed : None --> Checks if a user is inactive
        + GetUser : User --> returns the cached user gathered from clean
    """
    username = forms.CharField(max_length=32)
    password = forms.CharField(widget=forms.PasswordInput, max_length=32)
    error_messages = {
        'invalid_login' : ('This username and password combination was not found'),
        'inactive' : ('This account is inactive'),
    }

    def clean(self):
        """ clean
        Overriden clean method that verifies that the username and password
        are valid, but also checks to see if the user is active in the
        ConfirmLoginAllowed method

        Raises:
            - If the user was not found, then it will return the 
            'invalid_login' message
        """
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            self.user_cache = authenticate(username=username, password=password)

            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
            )
            else:
                self.ConfirmLoginAllowed(self.user_cache)

        return self.cleaned_data
    
    def ConfirmLoginAllowed(self, user):
        """ ConfirmLoginAllowed
        Called from the clean method, this method checks to see if the user is
        active before logging the user in

        Raises:
            - If the user is not active, it will return the error message for 
            'inactive'
        """
        if not user.is_active:
            raise forms.ValidationError(
                self.error_messages['inactive'],
                code='inactive',
            )

    def GetUser(self):
        """ GetUser
        Gets the user from the cached form data
        """
        return self.user_cache