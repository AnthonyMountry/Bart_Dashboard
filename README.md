# BART Dashboard

This project can be found at <https://github.com/harrybrwn/bart-dashboard>


An internal analytics dashboard and project management system for BART.

## Development

### Run the Backend

There are two options for setup:

1. [Run with docker and docker-compose](#setup-with-docker)
2. [Manual setup](#manual-setup)

> Note: setup will require access to a terminal to run the setup commands.

#### Setup with docker

- Install [docker](https://docs.docker.com/get-docker/) and [docker-compose](https://docs.docker.com/compose/install/)
- Create a `.env` file (see our example .env.example)
- Run the following command in a terminal in the bart-dashboard folder

```
docker-compose up
```

And that's all the setup needed using docker.

> Note: it will take a second to load the database file (db/postgres/database.dump)


#### Manual Setup

If you don't have docker installed it is more involved.

- [Install python 3](https://www.python.org/downloads/release/python-386/)
- Install dependencies

```sh
pip install -r requirements.txt
```

- Setup the database (first unzip the example data and put it in `/db`)

```sh
flask db init
flask db migrate
flask db upgrade
# clean and load the example data (this may take a while)
flask load-db
```

- Run the api

```sh
flask run --with-threads
```

Now we need build the frontend.

- [Install npm](https://www.npmjs.com/get-npm)

- Install dependencies

```sh
npm install
```

- Run the build system

```sh
npm build
```

### Testing

All the tests are in the `/tests` directory and can be run with the command:

```sh
pytest
```

---

## Database

See [database documentation](doc/db/README.md).

---

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
| [`/api/assets`](#Assets "/api/assets")                  | `GET`                          | List assets                           |
| [`/api/asset/<id>`](#Assets "/api/asset")               | `GET`, `POST`, `DELETE`, `PUT` | Manage a single asset                 |
| [`/api/asset/<id>/readings`](#Assets "/api/asset")      | `GET`                          | List an asset's meter readings        |
| [`/api/workorder/<id>`](#work-order "/api/workorder")   | `GET`, `POST`, `DELETE`, `PUT` | Manage work orders                    |
| [`/api/user`](#Users)                                   | `GET`, `POST`, `DELETE`, `PUT` | Manages users of the dashboard        |

### File Uploads

**POST** `/api/upload` Upload an excel spreadsheet or a csv file. This should be encoded as multipart form data.

The request can include the following url parameters.

- `?type=<type>` what type of data is being sent (i.e. MPU, Asset, Work Order)
- `?filename=<filename>` name of the file being uploaded

Returns an [error response](#error-responses)

---


### Assets

**GET** `/api/assets` List assets.

Url Parameter:

* `?limit=5` Limits the number of asset objects returned.
* `?offset=3` Offsets the response by the given number.
* `?search=<text>` Search for a keyword

<a name="example-assets-json">Example response:</a>

```json
{
  "assets": [
    {
      "bartdept": "AFC",
      "description": "COIN HANDLING",
      "num": 123456,
      "status": "OPERATING"
    },
    {
      "bartdept": "AFC",
      "description": "COIN HANDLING",
      "num": 123457,
      "status": "OPERATING"
    }
  ]
}
```

**GET** `/api/asset/<id>` Get an asset by ID.

<a name="example-asset-json">Example response:</a>

```json
{
  "bartdept": "AFC",
  "description": "COIN HANDLING",
  "num": 123456,
  "status": "OPERATING"
}
```

**POST** `/api/asset` Create a new asset.

Returns an [error response](#error-responses)

**PUT** `/api/asset/<id>` Update an asset.

Returns the updated [asset](#example-asset-json) or an [error response](#error-responses).

**DELETE** `/api/asset/<id>` Delete an asset.

Returns an [error response](#error-responses)

**GET** `/api/asset/<id>/readings` Get an asset with all of it's meter readings.

<a name="example-meter-reading-json">Example response:</a>

```json
{
  "bartdept": "AFC",
  "description": "COIN HANDLING",
  "num": 123456,
  "status": "OPERATING",
  "meter_readings": [
    {"reading": 10000001, "readingdate": "Thu, 16 Mar 2017 00:00:00 GMT"},
    {"reading": 10000002, "readingdate": "Fri, 17 Mar 2017 00:00:00 GMT"}
  ]
}
```

**POST** `/api/asset` Create a new asset by sending json data.

Responds with an [error response](#error-responses)

---

### Users

**GET** `/api/user` Get a user

* `?username=<username>` __Required__ username parameter
* `?password=<password>` __Required__ password parameter
* `?email=<email>` Sign in with email (alternative to `?username`)

**POST** `/api/user` Create a user.

Data must be sent as a JSON body. Returns status 201 on success.

```
POST /api/user
Content-Type: application/json

{
  "username": "test-user",
  "password": "<password>",
  "email": "test@test.com"
}
```

**PUT** `/api/user` Update a user

The new data for the user should be passed as a JSON request body.

* `?username=<username>` __Required__ username parameter
* `?password=<password>` __Required__ password parameter
* `?email=<email>` Sign in with email (alternative to `?username`)

**DELETE** `/api/user` Delete a user from the database

* `?username=<username>` __Required__ username parameter
* `?password=<password>` __Required__ password parameter
* `?email=<email>` Sign in with email (alternative to `?username`)

---

### Work Order

**GET** `/api/workorders` Get a list of assets

* `?limit=5` Limits the number of workorder objects returned.
* `?offset=3` Offsets the response by the given number.
* `?search=<text>` Search for a keyword

```json
[
  {
    "num": 123,
    "alias": "64-14-64700-0236",
    "asset_type": "AFC",
    "bartdept": "AFC",
    "description": "Repair 11-11-11110-0111 - UPS",
    "finish": "Wed, 29 Jan 2020 00:00:00 GMT",
    "labor_hours": 3.85,
    "location": "AFC-REPAIR",
    "material_cost": 0.0,
    "report_date": "Thu, 12 Dec 2019 00:00:00 GMT",
    "start": "Wed, 29 Jan 2020 00:00:00 GMT",
    "status": "CLOSE",
    "work_type": "CM"
  },
  {
    "alias": "64-14-88870-0442",
    "asset_type": "AFC",
    "bartdept": "AFC",
    "description": "Repair Ticket Transport Mechanism Entry",
    "finish": "Mon, 01 Jan 0001 00:00:00 GMT",
    "labor_hours": 0.0,
    "location": "AFC-REPAIR",
    "material_cost": 0.0,
    "num": 13968560,
    "report_date": "Thu, 21 Nov 2019 00:00:00 GMT",
    "start": "Wed, 19 Feb 2020 00:00:00 GMT",
    "status": "INPRG",
    "work_type": "CM"
  }
]
```

**GET** `/api/workorder/<wonum>` Get a specific work order by work order number

```json
{
  "num": 123,
  "alias": "64-14-64700-0236",
  "asset_type": "AFC",
  "bartdept": "AFC",
  "description": "Repair 01-01-11100-0111 - UPS",
  "finish": "Wed, 29 Jan 2020 00:00:00 GMT",
  "labor_hours": 3.85,
  "location": "AFC-REPAIR",
  "material_cost": 0.0,
  "report_date": "Thu, 12 Dec 2019 00:00:00 GMT",
  "start": "Wed, 29 Jan 2020 00:00:00 GMT",
  "status": "CLOSE",
  "work_type": "CM"
}
```

**DELETE** `/api/workorder/<wonum>` Delete a workorder

Responds with an [error response](#error-responses)

---

### MPU

MPU - Monthly Project Updates.

**GET** `/api/mpus` Returns a list of MPUs

Url Parameter:

* `?limit=5` Limits the number of MPU objects returned.
* `?offset=3` Offsets the response by the given number.
* `?search=<text>` Search for a keyword.

Example response:

```json
[
  {
    "id": "01SX001",
    "name": "Wheel Truing Machine",
    "ranking": 12,
  },
  {
    "id": "05OH000",
    "name": "ORY Control Tower 2nd Emeg Egr",
    "ranking": 43,
  },
  ...
]
```


**GET** `/api/mpu/<id>` Get an MPU by id.

<a name="example-mpu-json">Example response:</a>

```
{
  "id": "01SX001",
  "name": "Wheel Truing Machine",
  "ranking": 12,
}
```

**DELETE** `/api/mpu/<id>` Delete the monthly project update.

Returns an [error response](#error-responses)

**POST** `/api/mpu` Create a project record.

Returns an [error response](#error-responses)

**PUT** `/api/mpu` Create a project record.


------------------


<details>
  <summary>Not yet implemented...</summary>


#### MPU Milestones

**GET** `/api/mpu/<id>/milestone` Get the MPU milestone by id.

**DELETE** `/api/mpu/<id>/milestone` Delete an MPU milestone.

Returns an [error response](#error-responses)

**POST** `/api/mpu/<id>/milestone` Create a milestone for an MPU.

Returns an [error response](#error-responses)

**PUT** `/api/mpu/<id>/milestone` Update an MPU milestone.

---

#### MPU Funds

**GET** `/api/mpu/<id>/fund` Get the MPU fund by id.

**DELETE** `/api/mpu/<id>/fund` Delete an MPU fund.

Returns an [error response](#error-responses)

**POST** `/api/mpu/<id>/fund` Create a fund for an MPU.

Returns an [error response](#error-responses)

**PUT** `/api/mpu/<id>/fund` Update an MPU fund.

</details>

---

### Error Responses

If and endpoint does not return data, then it should return an error response as JSON.

```json
{
  "error": "This is a helpful error message, if something went wrong",
  "success": "This is a message saying that everything is ok",
  "debug": "More in-depth debugging message",
  "status": 404, // the http status of the response
  "code": 1234   // error code (0 for success)
}
```


## TODO

- [ ] Full database design and implementation
  - [x] Monthly Project Updates
  - [ ] Switch Throw counts
  - [x] Work orders
  - [x] Assets
  - [x] Meter readings
  - [x] Maybe a users table
- [ ] Authentication and authorization, see [this tutorial](https://dev.to/paurakhsharma/flask-rest-api-part-3-authentication-and-authorization-5935)
  - [x] use `flask_bcrypt` for hashing passwords
  - [ ] add different permission levels for BART employees
- [x] write a script that will populate the development database with the data from the excel spreadsheets
- [x] Write an `Error` class that will make returning json error easier (see [error responses](#error-responses)).
  - [ ] Think of other useful error fields that can be included in the [error responses](#error-responses) JSON response.
- [x] Use [pyexcel](https://github.com/pyexcel/pyexcel) for in-memory excel spreadsheets, [tutorial](http://docs.pyexcel.org/en/latest/tutorial06.html)
- [ ] Replace the MPU spreadsheets with a page on the dashboard (if bart wants that)
  - [ ] Add api endpoints that would replace all the excel macros in `UC Merced 2020 SE Project/Monthly Project Update - MPU/MPU_July 20_20200820.xlsm`

## Notes
* Here is the [query documentation](https://docs.sqlalchemy.org/en/13/orm/query.html) for interacting with the database using the ORM (SQLAlchemy). And here is a [tutorial](https://hackersandslackers.com/database-queries-sqlalchemy-orm/).
* This is an [example project](https://github.com/gothinkster/flask-realworld-example-app) for flask. This is [flask's documentation example](https://github.com/pallets/flask/tree/master/examples/tutorial)
* [More flask tutorials](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world)

## Terms

Here is a list of useful terms.

- _Asset_ - Some tool, machine, or vehicle that is used by BART.

- _MPU_ - _M_onthly _P_roject _U_pdate, a report generated for tracking internal projects

- _NonRev Vehicles_ - Vehicles that do not generate revenue (everything that isn't a train)

- _OCC_ - _O_perations _C_ontrol _C_enter, control stations that manage operations.

- _Meter_ - A machine that takes and records numeric readings.

- _Fare Gate_ - A machine that requires a ticket before letting one person board a train. These have a number of different meter-readings associated with them.

- _Switch Machine_ - A piece of the train track that switches the trains direction.

- _Throw count_ - The number of times a _switch machine_ has changed direction.

- _Work Order_ - A maintenance job. Common attributes of a WO are duration and cost.

<details>
  <summary>Other Acronyms...</summary>

  - _CM_ -(usually for a work order) Corrective maintenence

  - _PM_ - Preventative maintenance (usually for a work order)

  - _INSP_ - Inspection job (usually for a work order)

  - _NRVE_ - NonRev Vehicles (NRVE is a bartdept)

  - _AFC_ - Fare Gate equipment (AFC is a bartdept)

  - _ACTCOUNTL_ - Smart card and magnetic ticket transaction of actuator

  - _ACTCOUNTR_ - Smart card and magnetic ticket transaction of actuator

  - _COINSDT_ - Coins taken and coins dispensed of AFC vendor

  - _MTENTRY_ - Magnetic ticket entry in a fare gate

  - _MTEXIT_ - Magnetic ticket exit in a fare gate

  - _SCENTRY_ - Smart card entry

  - _SCEXIT_ - Smart card exit

  - _TRANSACTIO_ - Transaction count

</details>
