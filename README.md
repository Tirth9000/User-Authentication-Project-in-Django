
# Django User Authentication System

This project implements a secure and robust user authentication system in Django, featuring email registration with strong password constraints. Users can log in with their credentials, and in case of forgotten passwords, the system.
This project implements a secure and robust user authentication system in Django, featuring email registration with strong password constraints. Users can log in with their credentials, and in case of forgotten passwords, the system offers an OTP-based email verification process. The OTP is valid for 40 seconds, with a limit of three resend attempts.

To enhance performance, Celery is used to handle email notifications and OTP delivery asynchronously, reducing delays caused by the SMTP server. The system also integrates middleware for added security, ensuring safe access to all pages and information.


## Run Locally

Clone the project

```bash
https://github.com/Tirth9000/User-Authentication-Project-in-Django.git
```


Install dependencies

```bash
pip install django, celery, redis, pymysql(for mysql connectivity)
```

Apply makemigration 

```bash
python manage.py makemigrations 
python manage.py migrate
```

Start Redis and Celery server

```bash
brew services start redis
celery -A auth_app beat --loglevel=info
```


Start the server

```bash
python manage.py runserver
```

Now your app is ready.
## Environment Variables

To run this project, you will need to add the following environment variables to your .env file 

`EMAIL_HOST`

`EMAIL_PORT`

`EMAIL_HOST_USER`

`EMAIL_HOST_PASSWORD`


