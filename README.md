![FlaskRSS-Tests](https://github.com/Pytlicek/FlaskRSS/workflows/FlaskRSS-Tests/badge.svg)  [![codecov](https://codecov.io/gh/Pytlicek/FlaskRSS/branch/main/graph/badge.svg)](https://codecov.io/gh/Pytlicek/FlaskRSS) [![Sourcery](https://img.shields.io/badge/Sourcery-enabled-brightgreen)](https://sourcery.ai) [![Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)
## FlaskRSS
### Simple RSS downloader and keeper  

![](/app/static/images/screenshot_1.png "Example 1")  

![](/app/static/images/screenshot_2.png "Example 2")

## Install required PIP packages within Virtualenv
- Setup virtualenv: `virtualenv venv` 
- Activate virtualenv: `source venv/bin/activate` 
- Upgrade PIP package: `pip install -U pip` 
- Install PIP packages: `pip install -r requirements.txt` 

## Run App
- Run DB Seed at first time: `FLASK_ENV=development python3 ./db_seed.py`
- Run Flask App: `FLASK_ENV=development flask run`
