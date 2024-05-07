from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views import View

class CalendarView(View):

    def get(self, request: dict) -> HttpResponse:
        """ GET Handler
        The GET Handler for the Calendar works with the following url addresses
            - calendar/
            - calendar/weekly
            - calendar/monthly
            - calendar/*
        The only two of which the user cares about are calendar/weekly 
        and calendar/monthly. Any other address will route to /weekly as the
        default.

        It will check to see if the user is authenticated. If the user is
        logged in, it will determine if it will go to the weekly or monthly
        calendars. If the user is not authenticated, it will redirect to the
        login screen.
        """

        accepted_paths = {
            'monthly' : '/calendar/monthly',
            'weekly' : '/calendar/weekly', 
        }

        if request.user.is_authenticated:
            if request.get_full_path() == accepted_paths['monthly']:
                return self.__Monthly(request)
            elif request.get_full_path() == accepted_paths['weekly']:
                return self.__Weekly(request)
            elif request.get_full_path() not in accepted_paths:
                return redirect(accepted_paths['weekly'])
        else:
            return redirect('/login')
        
    def post(self, request: dict) -> HttpResponse:
        """ POST Handler
        """
        return HttpResponse("POST Calendar")
    
    def __Monthly(self, request: dict) -> HttpResponse:
        """ Monthly Calendar
        Right now this will load the monthly_calendar template 
        and pass the username
        """
        return render(request, 'calendar/monthly_calendar.html', {'user':request.user.username})

    def __Weekly(self, request: dict) -> HttpResponse:
        """ Weekly Calendar
        Right now this will load the weekly_calendar template 
        and pass the username
        """
        return render(request, 'calendar/weekly_calendar.html', {'user':request.user.username})