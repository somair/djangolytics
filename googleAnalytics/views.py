# Author: Douglas Anderson
# Derived from code sample here: http://bit.ly/1pE98F9

import os
import httplib2
# Django imports
#from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import HttpResponseBadRequest
# Google API imports
from apiclient.discovery import build
from oauth2client import xsrfutil
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.django_orm import Storage
# Project imports
from djangolytics import settings
from googleAnalytics.models import CredentialsModel


# Which apis the app is requesting access to
SCOPE = "https://www.googleapis.com/auth/analytics.readonly"
# Where should google return to after it has generated an Auth Code
#REDIRECT_URI = "http://localhost:8080/oauth2callback"
REDIRECT_URI = "http://sleepy-river-9090.herokuapp.com/oauth2callback"

FLOW = OAuth2WebServerFlow(client_id = os.environ["GA_CLIENT_ID"],
                           client_secret = os.environ["GA_CLIENT_SECRET"],
                           scope = SCOPE,
                           redirect_uri = REDIRECT_URI)

@login_required
def index(request):
    storage = Storage(CredentialsModel, "id", request.user, "credential")
    credential = storage.get()
    if credential is None or credential.invalid == True:
        # Initiate the OAuth process
        FLOW.params["state"] = xsrfutil.generate_token(settings.SECRET_KEY,
                                                       request.user)

        # Ask Google to generate an authorizing page
        authorize_url = FLOW.step1_get_authorize_url()
        return HttpResponseRedirect(authorize_url) # Go to Authorizing page
    else:
        http = httplib2.Http()  # Get a http object
        http = credentials.authorize(http) # Auth it with our fancy credentials
        service = build("analytics", "v3", http=http)
        accounts = service.management().accounts.list().execute()
        print accounts
        return render("YEPPPP")

@login_required
def auth_return(request):
    if not xsrfutil.validate_token(settings.SECRET_KEY,
                                   request.REQUEST["state"], request.user):
        return HttpResponseBadRequest()
    # Exchange the Auth code for a OAuth Token
    credential = FLOW.step2_exchange(request.REQUEST)
    storage = Storage(CredentialsModel, "id", request.user, "credential")
    storage.put(credential) # Store the token with reference to this user
    return HttpResponseRedirect("/")

