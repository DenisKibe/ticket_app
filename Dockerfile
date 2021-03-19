#set base image(host OS)
FROM python:3.8-slim

#set the working directory in the container
WORKDIR /home/kibe/ticket_app

#copy the dependencies file  to the working dir
COPY requirements.txt requirements.txt

#install dependencies
RUN apt-get update && apt-get install -y libpq-dev gcc
RUN pip install -r requirements.txt
RUN apt-get autoremove -y gcc

#copy the content of the  local src dir to the working dir
COPY . .

#command to run on container start
CMD ["gunicorn","--bind","0.0.0.0","main:app"]
