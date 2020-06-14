# image-labelling-app-api
Image labelling app API source code.

# Technologies used in this project
1. Python version 3.7
    - PEP-8 style guidlines is used for the Python code linting
2. Django Python web framework
    - Django ORM (Object Relational Mapper) is used for converting objects into database rows
    - Django Admin is used as an out-of-the-box admin site, managing objects and visualizing the database
3. Django Rest Framework
    - Used for built-in authentication
    - DRF viewsets are used for the structure of the API
    - DRF serializers are used to provide validation on our requests to our API and to convert JSON objects to Django database models
4. Postgres Database
    - An open source production grade DB
5. TDD (Test Driven Development)
    - TDD is used as my software development process
    - TDD increases test coverage and ensures that the tests work
    - TDD increases the quality of code and makes it easier to maintain and change the code 
    - TDD takes more time at writing the code but saves time in future and ensures a  testable and quality code
6. Docker virtualization tool
    - Docker helps to isolate code from the machine that it is running on
    - It is a super lightweight virtual machine
    - Docker is used to wrap my project and all it's dependencies that can be ran on any machine
    - The docker container can be used to deploy the project to a cloud platfrom like AWS, Microsoft Azure or Google Cloud 
7. Travis CI 
    - Travis CI is used to Automate linting and unit tests every time I made changes to my code 
    - Travis CI is a continuous integration tool that integrates with github 
    - Continuous integration helps identifing issues early
    - [![Build Status](https://travis-ci.org/IdaEdgeware/image-labelling-app-api.svg?branch=master)](https://travis-ci.org/IdaEdgeware/image-labelling-app-api)


# How to Install
1. Clone the project from GitHub 
2. Inside the main directory of the project Run docker container 
    - docker-compopse build
3. Run the database server
    - docker-comose up
4. The Admin page is accessible through 
    - http://127.0.0.1:8000/admin/
5. For creating a superuser to use the Admin page use the following command:
    - docker-compose run app sh -c "python manage.py createsuperuser"
    - The email and password that you enter after running this command can be used to log in the Admin page


# Manage User API Endpoints
| URL | Action |
 --- | --- |
| http://127.0.0.1:8000/api/user/create/ | Create a new user  |
| http://127.0.0.1:8000/api/user/token/| Enter the user email address and password and you'll get the authentication token. This token can be used for other actions that require authentication.|
| http://127.0.0.1:8000/api/user/me/| Modify information of a user|


# Image API Endpoints
| URL | Action |
| --- | --- |
| http://127.0.0.1:8000/api/image/  | Root view of the image api|
| http://127.0.0.1:8000/api/image/images/  | Retrieve the list of all images related to the authenticated user or create a new image|
|  http://127.0.0.1:8000/api/image/labels/| Retrieve the list of all labels related to the authenticated user or create a new label|
| http://127.0.0.1:8000/api/image/patientinfo/| Retrieve the list of all patient info related to the authenticated user or create a new patient info field to for the image|
| http://127.0.0.1:8000/api/image/labels/1/ | Retrieve or modify the image label by id |
| http://127.0.0.1:8000/api/image/patientinfo/1/| Retrieve or modify the patient info by id |
| http://127.0.0.1:8000/api/image/images/1/upload-file/| Upload image file for the image by id number|
| http://127.0.0.1:8000/api/image/images/?patient_info=1&labels=2/| Filter images by patient info and labels' ids|
|http://127.0.0.1:8000/api/image/images/?patient_info=1,2/| Filter image by patient info's id|
|http://127.0.0.1:8000/api/image/images/?labels=1,2/| Filter image by labels's id|


# How to Run Tests locally 
1. docker-compose run --rm app sh -c "python manage.py test && flake8"

# How to do actions that require authentication 
1. One way is using curl e.g. : curl -H "Authorization: Token 16ac3a73e653f73b65e0bf9809a37de5234b16ed" http://127.0.0.1:8000/api/image/labels/
2. Another way is using the ModHeader extention for Chrome. ModHeader is a Chrome extention that we can modify HTTP request and response headers.
