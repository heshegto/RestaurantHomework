# My homework for company Y_LAB:
## How to start testing it:
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
