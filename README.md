# BART Dashboard

An internal analytics dashboard and project managment system for BART.

## Development
* Install python 3
* Setup a virtual environment if you want (recomended for depenancy managment but still optional)
    * `python -m venv <your-environment-name>`
    * `<your-environment-name>/bin/activate` (for mac and linux)
* Install dependancies
```
pip install -r requirements.txt
```
* Run the backend
```
flask run
```
or
```
python -m flask run
```
* Other steps coming soon...


## TODO
- Pick between server side rendering or client side rendering
    - If we go with client side rendering, React or Angular are tools we should use
- write a script that will populate the development database with the data from the excel spreadsheets
