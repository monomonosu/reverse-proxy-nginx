FROM tiangolo/uwsgi-nginx-flask:python3.8

COPY /app /app
# For now test. Comment out when nessesary.
# COPY /app/main_test.py /app/main.py

RUN pip install reportlab
RUN pip install flask_cors
RUN pip install SQLAlchemy 
RUN pip install Flask-SQLAlchemy 
RUN pip install flask-marshmallow 
RUN pip install marshmallow-sqlalchemy
RUN pip install Flask-Migrate 
RUN pip install Pillow 
RUN pip install flask-login
RUN pip install python-dateutil

# Setup initial Database
#RUN rm -r migrations
#RUN rm  flask_sample.db
ENV  FLASK_APP models.py
RUN flask db init
RUN flask db migrate
RUN flask db upgrade
RUN python ./seeder.py
RUN cp /usr/share/zoneinfo/Japan /etc/localtime
