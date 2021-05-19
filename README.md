# Django-Stripe-Project
This application contains Django framework and Stripe payment gateway in which user can do login , logout , signup  and subcription . User can see its subscription plan is active or not, if user wants to cancel a subscription so they can do within trial period i.e. valid upto 7 days , after that user must have to pay $49.99.

Technology Stack :

1. Backend - Python ,Django, Postgresql Database

2. Frontend - HTML, CSS, Javascript, Bootstrap, Stripe payment gatewaysoftware

# Procedure

1.Install the requirements:

`pip install -r requirements.txt`

2. Create a .env file and give the values of all vaiable which is defined in .env.example.
3. Create a database.
4. Apply the migrations :

`python manage.py migrate`

5. Run the server :

`python manage.py runserver`
