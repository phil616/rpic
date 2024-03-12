from celery import Celery

redis_url = "redis://localhost:6379"

app = Celery("name",broker=redis_url)

app.send_task("task",args=["Hello World"],expires=)