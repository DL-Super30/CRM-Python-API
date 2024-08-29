FROM python:latest
WORKDIR /app
COPY . .
RUN pip install -r requirement.txt
COPY . .
RUN python manage.py migrate
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

