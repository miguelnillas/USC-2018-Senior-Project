from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views import View
from django.utils import timezone
from django.contrib.auth import authenticate, login
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User
from ..forms import LoginForm

class LoginView(View):

    def get(self, request:dict) -> HttpResponse:
        """ get
        The only render in the GET for the Login is the login page itself.
        We may build upon this later
        """
        if request.get_full_path() == '/login':
            return self.__DisplayLogin(request)

        else:
            return redirect('/login')

        
    def post(self, request:dict) -> HttpResponse:
        """ post
        Right now we know what we are going to POST, so we can handle it
        manually. If we end up expanding the decision tree, we can make this
        a POST handler and have it split into different methods 
        (see Manga Website)
        """
        if request.get_full_path() == "/login":
            return self.__VerifyLogin(request)
        else:
            return HttpResponse("You shouldn't be here")
        
    def __DisplayLogin(self, request:dict) -> HttpResponse:
        return render(request, 'login/login.html', {})

    def __VerifyLogin(self, request:dict) -> HttpResponse:
        """ Verify Login
        """
        user_form = LoginForm(request.POST)

        if user_form.is_valid():
            user = user_form.GetUser()
            if user is not None:
                return self.__SuccessfulLogin(request, user)
            else:
                return HttpResponse('unsuccessful login')
        else:
            return self.__FailedLogin(request, user_form)
            

    def __SuccessfulLogin(self, request:dict, user:User) -> HttpResponse:
        """ Successful Login
        """
        login(request, user)
        sessions = Session.objects.filter(expire_date__gte=timezone.now())
        uid_list = []

        # Build a list of user ids from that query
        for session in sessions:
            data = session.get_decoded()
            uid_list.append(data.get('_auth_user_id', None))

        # Query all logged in users based on id list
        logged_users = User.objects.filter(id__in=uid_list)
        return redirect('/calendar')

    def __FailedLogin(self, request:dict, user_form:LoginForm) -> HttpResponse:
        """ Failed Login
        """
        error_message = user_form.error_messages['invalid_login']
        return render(request, 'login/login.html', {'error_message':error_message})