The API is implemented fully through Django Rest Framework which is a powerful framework for back-end and API development by Python.

1.Set-up and run the project

For running the project on your machine, Firstly you need to ensure that you have Python and venv tool, which is a tool for managing python virtual environments, installed on your device. Then, you need to create an env by command: python3 -m venv env, then by source env/bin/activate you can activate your env. pip install -r requirements.txt will install all dependencies and make your environment ready to run the project.

After setting the environment up, you are ready to use the project on your own device. It can be easily done by the following commands:

python manage.py migrate
python manage.py runserver

Finally, after these commands the project will run on http://127.0.0.1:8000/.
