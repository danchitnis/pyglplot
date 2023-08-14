call env\Scripts\activate.bat
python -m pip install --upgrade --force-reinstall pyglplot --find-links=.\..\dist\
python testLine.py
python testRoll.py
python testScatter.py
deactivate