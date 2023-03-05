source ./env/bin/activate
python3 -m pip install --upgrade --force-reinstall pyglplot --find-links=./../dist/
python3 testLine.py
python3 testRoll.py
deactivate