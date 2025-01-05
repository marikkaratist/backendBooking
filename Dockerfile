FROM python:3.11.11

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

#CMD ["python", "src/main.py"]
CMD ["sh", "-c", "alembic upgrade head && python src/main.py"]
