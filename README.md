# PA06 - FlaskDo

> Submission Date: 30-08-2020 10:00am

## Submission

* Fork this repository [this](https://github.com/geokhoury/HTU-PA06-flaskdo) repository on your personal Github account.
* Commit often, and push your changes to Github. Remember to write good commit messages.
* Submit the link for your repository on **Microsoft Teams** under **Assignments**.
  * Remember to click the `Turn in` button :).

## FlaskDo

For this practical assignment you will be building a Flask-based To-Do list web application.

### General Notes

* Think about your data model. Use a paper and a pencil to design the data model.
* Write clear and concise comment lines.
* Follow the Python naming convention.
  * Use clear and descriptive names for your variables and methods.  
  * Use clear and descriptive names for your routes, views, and blueprints.
* Add any additional project requirements to `requirements.txt`.
* Use blueprints and views or organize your application routes and views.
* Use `sqlite3` to persist all of your data.

### Data Model

You are provided a basic data model under `models`. The provided model only defines the classes and their basic attributes.

* Define **getters** and **setters** for all of the **attributes**.
* Think about any additional **attributes**, or **methods** you may need.

The data model includes the following:

* `User` -- A basic user object. Use this for your sign up and authentication.
* `TaskList` -- A list of tasks with a name.
* `Task` -- A task has **title**, **priority**, **status**, and an optional **description**.
* `Priority` -- Always use this [enum](https://docs.python.org/3/library/enum.html) for the **priority** attribute.
* `Status` -- Always use this [enum](https://docs.python.org/3/library/enum.html) for the **status** attribute.

### Requirements

Below you are provided a list of high-level business requirements for this project.

#### User
* As a user, I am able to create an account providing a valid **email** and **password**.
* As a user, I am able to use my valid credentials to log into the application.
* As a user, I can edit my own profile to provide additional information like my **first** and **last** names.
* As a user, I am able to change my **email** and **password**.

#### Task List
* As a user, I can create a new task list with a name I choose.
* As a user, I can create more than one task list.
* As a user, I can edit the **name** of any of my task lists.
* As a user, I can delete any of my task lists.

#### Task
* As a user, I can create a new task with a **title**, and a **priority**.
* As a user, I can assign my task to any existing task list.
* As a user, I can edit the **title**, **description**, **priority**, **status** and **task list** assignment of any of my tasks.
* As a user, I can delete any of my tasks.