FROM python:3.11.9

WORKDIR /docker

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]

EXPOSE 5000
