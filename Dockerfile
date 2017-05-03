FROM resin/rpi-raspbian:latest
MAINTAINER eLiquidInventory team

# Install required packages and remove the apt cache when done
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y -q \
	python3 \	
        python3-dev \
        python3-setuptools \
        python3-pip \
        build-essential \
        supervisor \
        sqlite3  && \
        pip3 install -U pip setuptools && \
        rm -rf /var/lib/apt/lists/*

# install uwsgi
RUN pip3 install uwsgi

#install requirements
COPY requirements.txt /tmp/
RUN pip3 install --requirement /tmp/requirements.txt

# Custom Supervisord config
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

EXPOSE 80

COPY ./website /website

CMD ["/usr/bin/supervisord"]
