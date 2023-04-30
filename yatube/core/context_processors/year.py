import datetime


def year(request):
    return {'year': int((datetime.date.today()).year),
            }
