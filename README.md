# Ticketing-System-
A backend system for managing projects and tickets, with admin and staff user roles, ticket status tracking, and project-user assignments.




📦 Tech Stack
Backend: Django, Django REST Framework

Database: Default (MySQL/based on config)
Auth: Django's built-in User model




- 📌 Setup Instructions

1 - git clone https://github.com/vanshi1405/Ticketing-System-.git
  - cd Ticketing-System-
  
2  - python3 -m venv venv
  - source venv/bin/activate

3  - python manage.py makemigrations
 -  python manage.py migrate
  
4 - python manage.py runserver

5  - Base URL: http://localhost:8000/ticketing_sys/



- Users: `http://127.0.0.1:8000/ticketing_sys/users/`  
- Tickets: `http://127.0.0.1:8000/ticketing_sys/ticket/`  
- Projects: `http://127.0.0.1:8000/ticketing_sys/projects/`

