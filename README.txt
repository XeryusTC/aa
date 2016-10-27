#Install virtual environment for python
---------------------------------------
pip install virtualenv
cd my_project_folder
virtualenv venv

#Run environment and install packages
---------------------------------------
source venv/bin/activate
pip install -r requirements.txt

#Run program 
---------------------------------------
python main.py

#Notes:
+++++++++++++++++++++++++++++++++++
Teacher and course information is stored in teachers.yaml. 
Course information is stored in locations.yaml
