import httplib2
from apiclient.discovery import build
from googleAnalytics.models import CredentialsModel
from oauth2client.client import AccessTokenRefreshError
from oauth2client.django_orm import Storage

def get_user_credentials(user):
    """Retrives the users credentials from storage"""
    storage = Storage(CredentialsModel, "id", user, "credential")
    return storage.get() # load the user's credentials from storage

def get_service_object(credential):
    """Creates a service object for the google analytics api"""
    http = httplib2.Http()  # Get a http object
    http = credential.authorize(http) # Auth it with our fancy credentials
    return build("analytics", "v3", http=http)

def get_first_profile_id(service):
    """Returns the profile id of the user. Stolen from the tutorial:
        bit.ly/1wmZJqn"""
    try:
        # Get all the GA accounts associated with the service object's user.
        accounts = service.management().accounts().list().execute()
    except AccessTokenRefreshError:
        # The access token is stale. Should be storing the refresh tokens?
        return None
    if accounts and accounts.get('items'):
        firstAccountId = accounts.get('items')[0].get('id')
        # Get a webproperties list with the first account's id
        webproperties = service.management().webproperties().list(
                accountId=firstAccountId).execute()
        if webproperties and webproperties.get('items'):
            firstWebpropertyId = webproperties.get('items')[0].get('id')
            # Get a profiles list with the first webproperties' id
            profiles = service.management().profiles().list(
                    accountId=firstAccountId,
                    webPropertyId=firstWebpropertyId).execute()
            if profiles and profiles.get('items'):
                # Select and return the first profile id
                return profiles.get('items')[0].get('id')
    return None # One of the many previous steps have failed

def get_hourly_sessions(start_date, end_date, service, profile_id):
    return service.data().ga().get(
            ids='ga:' + profile_id,
            start_date=start_date,
            end_date=end_date,
            dimensions="ga:date,ga:hour",
            metrics='ga:sessions').execute()

