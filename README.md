# BART Dashboard

An internal analytics dashboard and project management system for BART.

## Development
* Install python 3
* (optional) Setup a virtual environment if you want (recommended for dependency management but still optional)
    * `python -m venv <your-environment-name>`
    * `<your-environment-name>/bin/activate` (for mac and linux)
* Install dependencies
```
pip install -r requirements.txt
```
* Run the backend
```
FLASK_APP=api/app.py flask run
```
or
```
FLASK_APP=api/app.py python -m flask run
```
* Other steps coming soon...


## TODO
- Pick between server side rendering or client side rendering
    - If we go with client side rendering, React or Angular are tools we should use
- write a script that will populate the development database with the data from the excel spreadsheets
