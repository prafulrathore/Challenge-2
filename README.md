# Challenge-2
This application is based on django and stripe interface in which there is a login , logout , signup  and subcription feature for authenticated user and trial subscription valid upto 7 days after that charges must be taken.

#Technology Stack :

I have used in my application,

1. Python 3
2. Django 2
3. Postgresql Database
4. Stripe software
6. Frontend - HTML, CSS, Javascript, Bootstrap

#Running Locally

Firstly, create virtual environment and create a django project then clone the repository to your local machine:

git clone https://github.com/prafulrathore/Challenge-2.git

Install the requirements:

`pip install -r requirements.txt`

create a .env file and define the variable with the values of .env.example file in root directory of project. 

Apply the database migrations:

python manage.py migrate

Load the initial data: `` Create administrator/super user:

`python manage.py createsuperuser`

Finally, run the development server:

`python manage.py runserver`

Note- The site will be available at 127.0.0.1:8000. `
