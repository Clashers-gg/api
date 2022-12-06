# API

## Connect to Database
Enter the SQL database with this command: `pipenv run python manage.py dbshell` from the `api` directory. 

## URLs
Django has a bunch of urls, so we get a path from Django to our project url. This path url is used by the JavaScript Fetch API to make HTTP requests in many different forms to the server. For example, path is a part of the post request, which is a form of an HTTP request. 

Our urls begins with: http://localhost:8000

### Port
Our server runs on this port: 8000

### Paths
Some of our paths are:
/accounts/login
/accounts/logout
/signup

## Running
To run the api, run `pipenv run serve`
