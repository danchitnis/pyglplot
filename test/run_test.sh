source ./env/bin/activate
python3 -m pip install --upgrade --force-reinstall pyglplot --find-links=./../dist/
python3 test1.py
deactivate