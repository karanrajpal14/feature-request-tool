# Feature Request Tool

I developed this tool for a coding competition and it draws it's inspiration from Trello. It allows you to keep track of Feature Requests that you get from your clients. This uses [Flask][1] for the backend along with SQLite (which can be changed in the `.env` file thanks to [SQLAlchemy][2]) and [KnockoutJS][3] with other basic web technologies for the frontend. [Vagrant][4] is used for deploying the project as I have always wanted to play around with it.

Also, you can check out the for the project is deployed on Heroku.

## [Demo][5]

Send me a PR or raise an issue if you think that I've approached any aspect of the project incorrectly. As this was my first time working with this stack, bugs and mistakes are probable, sadly.

## Dependencies

- Flask
- KnockoutJS
- SQLite
- Vagrant

## Setup Instructions

### Prerequisites

- Python 3
- Vagrant
- Virtualbox

### Instructions

#### Running using Vagrant

- Clone the repo and as stated, make sure you have Vagrant and [Virtualbox][6] installed.
- Edit the `.env.sample` with your as per your requirements and rename it to `.env`. This is important as the project does make use of these variables.
- `cd` into the repo and run `vagrant up`. Meanwhile, grab some coffee as the first run takes a while depending on your internet connection.
- This installs all the required dependencies to run the project on a fresh VM. Once finished you can open `http://10.0.0.5` (which can be changed inside the `Vagrantfile`) in your browser and play around with the deployed project. Use `vagrant ssh` to access the VM environment.

#### Running locally

If you do not wish to run this project using Vagrant, you could just clone it and run it locally.

- Clone the repo and `cd` into the `frt` directory where the application lives
- Create a virtualenv by executing `python3 -m venv frt_env`
- Once the env is created, you can activate it by executing `source frt_env/bin/activate`
- Install all the dependencies by executing `pip install -r requirements.txt`
- Edit the `.env.sample` with your as per your requirements and rename it to `.env`. This is important as the project does make use of these variables.
- Make sure your database is set up and the `DATABASE_URL` is set in the `.env`
- Execute `python migrate.py db migrate` to build the migrations for the DB
- Execute `python migrate.py db upgrade` to commit the migrations to your db
- If you wish, run `flask addmockdata` to add a couple of entries to the database initially
- Tests can be run by executing `python -m unittest discover -s tests -p "test_*.py"` or by running the included `test_codebase.sh` script if you are lazy like me
- Run the local server by executing `flask run` and open `http://localhost:5000` in your browser

[1]: http://flask.pocoo.org/
[2]: https://www.sqlalchemy.org/
[3]: https://knockoutjs.com/
[4]: https://www.vagrantup.com/
[5]: https://feature-request-tool.herokuapp.com/
[6]: https://www.virtualbox.org/