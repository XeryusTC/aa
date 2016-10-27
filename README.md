Make sure to use python 3, not python 2 which is the default for most unix
operating systems.
#Install virtual environment for python
---------------------------------------
```
pip install virtualenv
cd my\_project\_folder
virtualenv venv --python=python3
```

#Run environment and install packages
---------------------------------------
```
source venv/bin/activate
pip install -r requirements.txt
```

#Run program 
---------------------------------------
python main.py

#Notes:
+++++++++++++++++++++++++++++++++++
Teacher and course information is stored in teachers.yaml. 
Course information is stored in locations.yaml
