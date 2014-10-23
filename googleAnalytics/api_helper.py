import httplib2
from apiclient.discovery import build

def get_service_object(credential):
    """Creates a service object for the google analytics api"""
    http = httplib2.Http()  # Get a http object
    http = credential.authorize(http) # Auth it with our fancy credentials
    return build("analytics", "v3", http=http)

def get_first_profile_id(service):
    """Returns the profile id of the user. Stolen from the tutorial:
        bit.ly/1wmZJqn"""
    # Get all the GA accounts associated with the service object's user.
    accounts = service.management().accounts().list().execute()
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

def get_hourly_sessions(start_datetime, end_datetime, service, profile_id):
    start_date_str = datetime.strftime(start_datetime, "%Y-%m-%d")
    end_date_str = datetime.strftime(end_datetime, "%Y-%m-%d")
    return service.data().ga().get(
            ids='ga:' + profile_id,
            start_date=start_date_str,
            end_date=end_date_str,
            dimensions="ga:date,ga:hour",
            metrics='ga:sessions').execute()

