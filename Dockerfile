FROM ubuntu

RUN apt-get update
RUN apt-get install -y python3.8 python3-pip curl

WORKDIR /tmp
ADD https://github.com/mcostalba/Stockfish/archive/master.tar.gz .
RUN tar -zxf master.tar.gz && \
    cd Stockfish-master/src && \
    make profile-build ARCH=x86-64 && \
    make install

WORKDIR /root
COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY peixsec/peixsec.py peixsec.py

ENTRYPOINT python3 peixsec.py
