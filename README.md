# SWEN-A2
1. Make sure you have python and pip installed. 
    -  Enter `py --version` and check that you have at least version 3.10.5 
2. Setup a virtual environment (venv) for python package management
    - Using CMD in this directory, run:
        - `py -m venv .`, this will create the venv
        - `Scripts\activate`, this will activate the venv
    - You can leave this environment by entering `deactivate` in the CMD
    - See https://realpython.com/python-virtual-environments-a-primer/#activate-it for more
3. Install project dependencies 
    - Run `pip install -r requirements.txt`, this will install any python packages for this project
    - Whenever you install a python package, run `pip freeze > requirements.txt` to save package changes to the requirements.txt
    - See https://learnpython.com/blog/python-requirements-file/ for more
4. Follow instructions on https://dev.mysql.com/doc/mysql-installation-excerpt/5.7/en/windows-installation.html to install mysql locally.
    - When setting the password for the root user, add it to the `.env` file as `SQL_PASSWORD={insert password here}`
6. Run `py update_sql.py`
    - This will attempt a sql connection and setup a database and insert some test data
5. Run `flask run`
    - This should start the flask server
    - Visit http://localhost:5000/
        - it should say 'hello world'
    - Visit http://localhost:5000/test
        - This should return the test data entered in step 6

