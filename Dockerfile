FROM python:3.6-slim

#ENV APP_HOME /app
#WORKDIR $APP_HOME
COPY . ./
RUN pip install -r requirements.txt
RUN pip list

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 'data_system:create_app()'
