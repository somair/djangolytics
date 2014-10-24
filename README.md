
# Djangolytics

This Django app aquired hourly data from the Google analytics api and displays
the number of sessions per hour by day of the week in a dot chart. This gives
insight into when your page is being viewed.

[Take a look here][APP_URL]

## Manual testing

To test the app you need a google account with Google analytics collecting
data. Follow the proceeding steps:

1. login to the site with one of username-password pairs
2. authenticate with google
3. click the "update database" link. Enter a range of dates. (e.g. "2014-01-01"
   and "2014-10-20"). click "query api" button. After the data is gathered from
   the api it will be inserted into the database, and you will be redirected to
   the home page.
4. click the "view dot chart" link. Enter a range of dates and click "query
   database". The page will then draw you a lovely dot chart.

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
