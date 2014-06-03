from celery import Celery
#//Settings module stuff
BROKER_HOST = "amqp://dss-radio:Ku9hwTn0XT5Xo@localhost:5672//"
#//Settings module stuff

app = Celery('server', BROKER_HOST)

@app.task
def add(x, y):
	return x + y



