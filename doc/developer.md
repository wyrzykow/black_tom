Guide For Black TOM Developers
==============================


Getting Started
---------------
### How to get a working, local, developer copy of BlackTOM
Get the `python 3.7+` virtual environment ready. Following commands suppose usage
of the [`pyenv` python version and virtual environments manager](https://github.com/pyenv/pyenv)
– recommended.  
 
```bash
cd ~/src
git clone https://github.com/wyrzykow/black_tom.git
cd black_tom  
git checkout akond-tests
pyenv install black_tom
pyenv local black_tom
pip install -r requirements.txt 
cd black_tom/
cp black_tom/local_settings.template.py black_tom/local_settings.py
./manage.py migrate
./manage.py createsuperuser
./manage.py runserver
``` 

What to Read
------------
* [TOM toolkit documentation](https://tom-toolkit.readthedocs.io/en/latest/introduction/getting_started.html)


