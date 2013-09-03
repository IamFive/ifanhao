icomic
===========

- install uwsgi server on your vm (nginx+uwsgi/apache+mod_uwsgi)
- install python requirements
	- suggest use python env, you can create one ``virtualenv icomic``
	- option, if u use env, activate it
	- ``cd code_root``
	- ``pip install -r requirements``

- bind icomic to wsgi server, script file is ``wsgi.py`` under project root
- for test purpose, you can cd project root, and run ``manage.py runserver --no-reload``