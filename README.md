
# Djangolytics

This Django app aquired hourly data from the Google analytics api and displays
the number of sessions per hour by day of the week in a dot chart. This gives
insight into when your page is being viewed.

[Take a look here][APP_URL]

## Local development

Development on your local machine is extremely constrained because the user
need to be authorized by google and they require a list of registered OAuth
callback urls.

- git clone the repo
- (optional) set up a virtualenv
- run `pip install` to gather dependencies
- run the tests with `python manage.py test --settings=djangolytics.test_settings`
- run the server with `foreman start`

## Heroku deployment

This app is designed to be deployed to heroku.

- To push new changes to heroku use the command `git push heroku master`
- The following environment variables need to be defined.
    - APP_SECRET_KEY   : any random string
    - GA_CLIENT_ID     : The id provided by the google Api dashboard
    - GA_CLIENT_SECRET : The client secret created by the google Api dashboard

## Requirements

- Python 2.7
- Django 1.7

[APP_URL]: http://sleepy-river-9090.herokuapp.com/
