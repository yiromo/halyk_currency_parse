FROM python:3.9

WORKDIR /src

COPY requirements.txt .
COPY ./src ./src

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "./src/main.py"]