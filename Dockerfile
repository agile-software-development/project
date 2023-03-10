FROM python:3-alpine
WORKDIR /app
COPY requirements.txt /app
RUN pip3 install -r requirements.txt --no-cache-dir
COPY . /app
ENTRYPOINT ["python3"]
EXPOSE 80
CMD ["manage.py", "runserver", "0.0.0.0:80"]