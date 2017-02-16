FROM ubuntu:latest
MAINTAINER Nicholas Koulopoulos "nickkoul13@gmail.com"
RUN apt-get update -y
RUN apt-get install -y python python-pip python-dev build-essential
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["app.py"]

EXPOSE 5000
