from django.urls import path

from frontend.views import LoginView
from frontend.views import CalendarView

""" NOTE
The paths for the frontend of the website include:
    - '' --> base path (which routes to the login for now)
    - 'login' --> the login page
    - 'calendar' --> For now, routes to the weekly calendar
    - 'calendar/weekly' --> Displays the weekly calendar
    - 'calendar/monthly' --> Displays the monthly calendar
"""
urlpatterns = [
    path('', LoginView.as_view()),
    path('login', LoginView.as_view()),
    path('calendar/', CalendarView.as_view()),
    path('calendar/weekly', CalendarView.as_view()),
    path('calendar/monthly', CalendarView.as_view())
]

