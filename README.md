# consul_fastapi


## To run this project:
### First, make sure you have Consul running locally. You can run Consul using Docker:
```
docker run -d -p 8500:8500 --name consul consul:latest
```
### Install the required dependencies:
```
pip install -r requirements.txt
```
### Run the FastAPI application:
```
python main.py
```