
def get_first_profile_id(service):
    """Stolen from the tutorial """ # TODO what tutorial?
    accounts = service.management().accounts().list().execute()

    if accounts.get('items'):
        firstAccountId = accounts.get('items')[0].get('id')
        webproperties = service.management().webproperties().list(
                accountId=firstAccountId).execute()
        if webproperties.get('items'):
            firstWebpropertyId = webproperties.get('items')[0].get('id')
            profiles = service.management().profiles().list(
                    accountId=firstAccountId,
                    webPropertyId=firstWebpropertyId).execute()
            if profiles.get('items'):
                return profiles.get('items')[0].get('id')
    return None

