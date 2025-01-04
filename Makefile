run:
	- python3 manage.py runserver 0.0.0.0:8004
kill: 
	- pkill -f "python3 manage.py runserver"
always:
	- nohup python3 manage.py runserver 0.0.0.0:8004 > output.log 2>&1 &
venv:
	- source venv/bin/activate