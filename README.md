# My homework for company Y_LAB:
## How to start testing 3 homework:
1) Clone repository:<br/>
`git clone https://github.com/heshegto/RestaurantHomework.git`
2) Install required packages:<br/>
`pip install -r requirements.txt`
3) Run `pre-commit` installation:<br/>
`pre-commit install`
4) Run `pre-commit` check:<br/>
`pre-commit run --all-files`
5) Change parameters in `.env` file if you need
6) Run app image build:<br/>
`docker-compose -f docker-compose.yml up --build -d`
7) Run test image build:<br/>
`docker-compose -f docker-compose-pytest.yml up --build -d`
<br/><br/>
* Task 6 implemented in tests/reverse.py
* Changes in pre-commit-config.yaml:<br/>
~ flake8 version changed 6.0.0 -> 6.1.0<br/>
~ mypy added string 'additional_dependencies: [types-redis==4.6.0.3]'


## How to start testing 2 homework:
1) Clone repository:<br/>
`git clone https://github.com/heshegto/RestaurantHomework.git`
2) Change parameters in `.env` file
3) Run image build:<br/>
`docker-compose up --build -d`
4) Run tests:<br/>
`docker-compose run tests`

## How to start testing 1 homework:
1) Clone repository:<br/>
`git clone https://github.com/heshegto/RestaurantHomework.git`
2) Create virtual environment if you need it:<br/>
`python -m venv venv`
3) Install required packages:<br/>
`pip install -r requirements.txt`
4) Run your PostgreSQL server
5) Change string `SQLALCHEMY_DATABASE_URL` with your database properties in `sql_app/database.py` file. Set `host`,
`port` and `database_name`, if you need it set `username` and `password`
6) Start API:<br/>
`uvicorn app.main:app --reload`
7) Start testing with Postman
