## How to run Restaurant API:
1) Clone repository:<br/>
`git clone https://github.com/heshegto/RestaurantHomework.git`
2) Install required packages:<br/>
`pip install -r requirements.txt`
3) Change parameters in `.env` file if you need
4) Run app image build:<br/>
`docker-compose -f docker-compose.yml up --build -d`
5) Run test image build if you need:<br/>
`docker-compose -f docker-compose-pytest.yml up --build -d`
