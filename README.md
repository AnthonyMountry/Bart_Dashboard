# BART Dashboard

An internal analytics dashboard and project management system for BART.

## API

### Overview

| endpoint                                                | methods                        | description                           |
| ------------------------------------------------------- | ------------------------------ | ------------------------------------- |
| [`/api/upload`](#File-Uploads "/api/upload")            | `POST`                         | Upload new data in bulk               |
| [`/api/mpu/<id>`](#MPU "/api/mpu")                      | `GET`, `POST`, `DELETE`, `PUT` | Monthly project updates (MPU)         |
| [`/api/mpus`](#MPU "/api/mpus")                         | `GET`                          | Get a list of monthly project updates |
| [`/api/mpu/<id>/milestone`](#MPU-milestones "/api/mpu") | `GET`, `POST`, `DELETE`, `PUT` | MPU milestones                        |
| [`/api/mpu/<id>/fund`](#MPU-funds "/api/mpu")           | `GET`, `POST`, `DELETE`, `PUT` | MPU Funds                             |
| [`/api/mpu/<id>/criteria`](#MPU "/api/mpu")             | `GET`, `POST`, `DELETE`, `PUT` | MPU Ranking criteria                  |
| [`/api/asset/<id>`](#Assets "/api/asset")               | `GET`, `POST`, `DELETE`, `PUT` | Manage a single asset                 |
| [`/api/workorder/<id>`](#work-order "/api/workorder")   | `GET`, `POST`, `DELETE`, `PUT` | Manage work orders                    |

### File Uploads

**POST** `/api/upload` Upload an excel spreadsheet or a csv file. This should be encoded as multipart form data.

The request can include the following url parameters.

- `?type=<type>` what type of data is being sent (i.e. MPU, Asset, Work Order)
- `?filename=<filename>` name of the file being uploaded

---

### MPU

MPU - Monthly Project Updates.

**GET** `/api/mpus` Returns a list of MPUs

Example response:

```json
[
  {
    "id": "01SX001",
    "name": "Wheel Truing Machine",
    "criteria_ranking": 12,
  },
  {
    "id": "05OH000",
    "name": "ORY Control Tower 2nd Emeg Egr",
    "criteria_ranking": 43,
  },
  ...
]
```

**GET** `/api/mpu/<id>` Get an MPU by id.

**DELETE** `/api/mpu/<id>` Delete the monthly project update.

**POST** `/api/mpu` Create a project record.

**PUT** `/api/mpu` Create a project record.

#### MPU Milestones

**GET** `/api/mpu/<id>/milestone` Get the MPU milestone by id.

**DELETE** `/api/mpu/<id>/milestone` Delete an MPU milestone.

**POST** `/api/mpu/<id>/milestone` Create a milestone for an MPU.

**PUT** `/api/mpu/<id>/milestone` Update an MPU milestone.

#### MPU Funds

**GET** `/api/mpu/<id>/fund` Get the MPU fund by id.

**DELETE** `/api/mpu/<id>/fund` Delete an MPU fund.

**POST** `/api/mpu/<id>/fund` Create a fund for an MPU.

**PUT** `/api/mpu/<id>/fund` Update an MPU fund.

---

### Assets

_TODO_

---

### Work Order

_TODO_

---

## Development

- Install python 3
- (optional) Setup a virtual environment if you want (recommended for dependency
  management but still optional)
  - `python -m venv <your-environment-name>`
  - `<your-environment-name>/bin/activate` (for mac and linux)
- Install dependencies `pip install -r requirements.txt`
- Run the backend `FLASK_APP=api/app.py flask run` or `FLASK_APP=api/app.py python -m flask run`
- Other steps coming soon... maybe... probably...

## TODO

- [ ] Authentication and authorization, see [this tutorial](https://dev.to/paurakhsharma/flask-rest-api-part-3-authentication-and-authorization-5935)
- [ ] Full database design and implementation
- [ ] write a script that will populate the development database with the data from the excel spreadsheets
- [ ] Pick between server side rendering or client side rendering
  - If we go with client side rendering, React or Angular are tools we could use

* [x] Use [pyexcel](https://github.com/pyexcel/pyexcel) for in-memory excel
      spreadsheets
  - Look at [this tutorial](http://docs.pyexcel.org/en/latest/tutorial06.html)

- [this project](https://github.com/gothinkster/flask-realworld-example-app) is a fat flask example app
