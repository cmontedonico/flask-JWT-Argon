FROM ubuntu:latest
RUN apt-get update -y
RUN apt-get install -y python3-pip python-dev
COPY . /app
WORKDIR /app
RUN pip3 install -r requirements.txt
ENTRYPOINT ["python3"]
CMD ["server.py"]