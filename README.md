# <img src="/public/to-do-list.png" alt="" width="40" hight="40"/> To-Do List Backend API

<!-- TABLE OF CONTENTS -->

## Table of Contents

- [:notebook_with_decorative_cover:About the project](#notebook_with_decorative_coverabout-the-project)
  - [🛠️Technologies](#🛠️technologies)
  - [📑Business rules](#�business-rules)
  - [:card_file_box:Database Schema](#card_file_boxdatabase-schema)
  - [:truck:Endpoints](#truckendpoints)
- [:book:General instructions](#bookgeneral-instructions)
  - [:electric_plug:Installation](#electric_pluginstallation)
- [:book:Usage Examples](#bookusage-examples)
- [:technologist:Developer](#technologistdeveloper)

<!-- ABOUT THE PROJECT -->

## :notebook_with_decorative_cover:About the project

Welcome to the backend API documentation for our To-Do List application! This API is built using Python and Flask, with SQLite as the database engine. Swagger has been integrated for easy and comprehensive API documentation.

### 🛠️Technologies

<ul>
  <li>Python 3.1.2</li>
  <li>Flask 3.0.0</li>
  <li>SQLite</li>
</ul>

### 📑Business rules

- A user can see all tasks;
- A user can add a new task;
- A user can update a task as 'done' or 'not done';
- A user can delete a task;

### :card_file_box:Database Schema

```
{
    id: Integer
    description: string
    done: (Integer, default=0)
}
```

### :truck:Endpoints

- User Endpoints

| URL / ENDPOINT | VERB   | DESCRIPTION      |
| -------------- | ------ | ---------------- |
| /tasks         | GET    | Return all Tasks |
| /task          | POST   | Create a Task    |
| /task          | PATCH  | Update a Task    |
| /task/?id=     | DELETE | Delete a Task    |

<!-- GETTING STARTED -->

## :book:General instructions

Below are the instructions for the installation, configuration, and use of the application.

### :electric_plug:Installation

1. Clone the repo

```sh
   git clone git@github.com:ANNEBORTOLI/puc-sprint1-backend.git
   cd puc-sprint1-backend
```

2. Create a virtal environmnet. Check the link below:

`https://virtualenv.pypa.io/en/latest/installation.html`

3. Installing Packages

```sh
    pip install requirements.txt
```

4. Run the Application locally

```sh
  (env)$ flask run --host 0.0.0.0 --port 5000
```

5. Run in development mode

```sh
  (env)$ flask run --host 0.0.0.0 --port 5000 --reload
```

6. Open the URL in your browser

```
  http://localhost:5000/
```

## :camera_flash:Usage Examples on Swagger

- Tasks List
<div align="center">
  <img src="/public/back-swagger-routes.png">
</div>
<br>

- Tasks List (JSON)
<div align="center">
  <img src="/public/tasks.png">
</div>
<br>

## :technologist:Developer

- [Github](https://github.com/ANNEBORTOLI)
- [Linkedin](https://www.linkedin.com/in/anne-bortoli/)
