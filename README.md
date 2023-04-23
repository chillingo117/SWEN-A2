# SWEN-A2
1. Follow instructions on https://dev.mysql.com/doc/mysql-installation-excerpt/5.7/en/windows-installation.html to install mysql locally.
2. Make sure you have python installed. 
    -  Enter `py --version` and check that you have at least version 3.10.5 
3. Setup a virtual environment (venv) for python package management
    - Using CMD in this directory, run:
        - `py -m venv .`, this will create the venv
        - `Scripts\activate`, this will activate the venv
    - You can leave this environment by entering `deactivate` in the CMD
    - See https://realpython.com/python-virtual-environments-a-primer/#activate-it for more
4. Run `pip install -r requirements.txt`
    - This will install any python packages for this project
    - Whenever you install a python package, don't forget to run `pip freeze > requirements.txt` to save package changes to the requirements.txt
    - See https://learnpython.com/blog/python-requirements-file/ for more

