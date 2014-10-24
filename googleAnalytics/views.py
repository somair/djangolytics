# Author: Douglas Anderson
# Derived from code sample here: http://bit.ly/1pE98F9

import os
from datetime import date
# Django imports
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import HttpResponseBadRequest
# Google API imports
from oauth2client import xsrfutil
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.django_orm import Storage
# Project imports
from djangolytics import settings
from googleAnalytics.models import CredentialsModel
from googleAnalytics.models import HourlyDataModel
from googleAnalytics.forms import StartEndDateForm
from googleAnalytics.api_helper import get_user_credentials
from googleAnalytics.api_helper import get_service_object
from googleAnalytics.api_helper import get_first_profile_id
from googleAnalytics.api_helper import get_hourly_sessions
from googleAnalytics.utils import create_date_from_str


# Which apis the app is requesting access to
SCOPE = "https://www.googleapis.com/auth/analytics.readonly"
# Where should google return to after it has generated an Auth Code
REDIRECT_URI = "http://sleepy-river-9090.herokuapp.com/oauth2callback"

FLOW = OAuth2WebServerFlow(client_id = os.environ["GA_CLIENT_ID"],
                           client_secret = os.environ["GA_CLIENT_SECRET"],
                           scope = SCOPE,
                           redirect_uri = REDIRECT_URI)

# TODO combine a few of these views to reduce the number of urls used.

@login_required
def index(request):
    credential = get_user_credentials(request.user) # Attempt to load the user's credentials
    if credential is None or credential.invalid == True:
        # User not authenticated. Initiate the OAuth process
        FLOW.params["state"] = xsrfutil.generate_token(settings.SECRET_KEY,
                                                       request.user)
        # Ask Google to generate an authorizing page
        authorize_url = FLOW.step1_get_authorize_url()
        return HttpResponseRedirect(authorize_url) # Go to Authorizing page
    else:
        # User is authenticated
        service = get_service_object(credential)
        profile_id = get_first_profile_id(service)
        return render_to_response("googleAnalytics/index.html", {
            "profile_name": None,
            "sessions": None
            })

@login_required
def dot_chart(request):
    query_result = HourlyDataModel.objects.all()
    return render_to_response("googleAnalytics/dot_chart.html", {
            "query_result": query_result
        })

@login_required
def hit_api(request):
    credential = get_user_credentials(request.user) # get user credentials
    if credential is None or credential.invalid == True:
        # User is not authorized. Go to the index to get authorized.
        return HttpResponseRedirect("/")
    else:
        # User is authorized.
        service = get_service_object(credential)
        profile_id = get_first_profile_id(service)

        if request.method == "GET":
            date_pick_form = StartEndDateForm()
            return render(request, "googleAnalytics/pick_date.html",
                          {"form": date_pick_form})
        else:
            # The request is POST
            date_pick_form = StartEndDateForm(request.POST)
        if not date_pick_form.is_valid():
            return render(request, "googleAnalytics/pick_date.html",
                          {"form": date_pick_form})

        # Query the API
        results = get_hourly_sessions(request.POST["start_date"],
                                      request.POST["end_date"],
                                      service, profile_id)
        rows = results.get("rows")
        for row in rows:
            row_date = create_date_from_str(row[0], "%Y%m%d")
            row_hour = int(row[1])
            row_sessions = int(row[2])
            # create a model if it does not exist for that date and hour
            HourlyDataModel.objects.get_or_create(date = row_date,
                                        hour = row_hour,
                                        defaults={"num_sessions":row_sessions})
        # TODO communicate that the db has been updated better. With messages.
        return HttpResponse("Database updated")


@login_required
def auth_return(request):
    if not xsrfutil.validate_token(settings.SECRET_KEY,
                                   request.REQUEST["state"], request.user):
        return HttpResponseBadRequest()
    # Exchange the Auth code for a OAuth Token
    credential = FLOW.step2_exchange(request.GET)
    storage = Storage(CredentialsModel, "id", request.user, "credential")
    storage.put(credential) # Store the token with reference to this user
    return HttpResponseRedirect("/")

