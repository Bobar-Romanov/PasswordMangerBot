FROM python:3.8-slim-buster



COPY . /app
RUN pip3 install -r /app/requirements.txt
WORKDIR /app

ENV MYSQL_HOST=db
ENV MYSQL_USER=root
ENV MYSQL_PASSWORD=root
ENV MYSQL_DATABASE=password_manager_db

ENV PMBTOKEN=6232290157:AAGCtDeM_57GSY3R25pKu9xNjjbV8yWbhJU
ENV DELAY_FOR_DELETE=60

CMD ["python","main.py"]