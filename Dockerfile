FROM ubuntu

RUN apt-get update
RUN apt-get -y install python3.8 python3-pip stockfish

COPY requirements.txt .

RUN pip3 install -r requirements.txt

ENTRYPOINT python3 service.py
