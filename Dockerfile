FROM python:3.10

WORKDIR /app

COPY requirements/requirements.txt .

RUN pip install -r requirements.txt

COPY /data ./data
COPY /app ./app
COPY run.py .

EXPOSE 8050

CMD ["python3", "run.py"]