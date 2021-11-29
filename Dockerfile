FROM ubuntu:20.04

LABEL "name"="NelectMon"
LABEL version="1.0"
LABEL description="This dockerfile is for creating image of the application itself. This image is capable for recieveing and vieweing data. It doesn't do the DB writing. It just ship the insert query to the queue."
LABEL "author"="Fahad Ahammed"

RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev build-essential

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip3 install -r requirements.txt

COPY . /app

EXPOSE 11000

ENTRYPOINT [ "python3" ]
CMD [ "run.py" ]