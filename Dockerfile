FROM python:3.8

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE 1

RUN mkdir /app
WORKDIR /app


COPY requirements.txt /app/
RUN pip install -r requirements.txt
COPY . .

#COPY ./docker-entrypoint.sh /

#RUN chmod +x /docker-entrypoint.sh

#RUN useradd -s /bin/bash postgres
#
#FROM library/postgres
#ENV POSTGRES_USER postgres
#ENV POSTGRES_PASSWORD postgres
#ENV POSTGRES_DB fpl_data
#USER postgres
#
#ENTRYPOINT ["/docker-entrypoint.sh"]
#
#EXPOSE 5432
#CMD ["postgres"]