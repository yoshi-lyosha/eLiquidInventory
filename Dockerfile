FROM resin/rpi-raspbian:latest
MAINTAINER eLiquidInventory team

RUN \
	apt-get update && \
	apt-get install -y -q python-dev python-setuptools build-essential
	
RUN easy_install pip
RUN pip install uwsgi

#install requirements
COPY requirements.txt /tmp/
RUN pip install --requirement /tmp/requirements.txt

# Install Supervisor
RUN apt-get update && apt-get install -y supervisor && rm -rf /var/lib/apt/lists/*

# Custom Supervisord config
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

EXPOSE 80

COPY ./website /website

CMD ["/usr/bin/supervisord"]
