FROM resin/rpi-raspbian

ENTRYPOINT ["/usr/bin/python", "-u", "qrlabs.py"]

WORKDIR /root/qrlabs

RUN apt-get update && apt-get install -y python-pip && pip install Flask && pip install gevent && pip install reportlab

COPY source .
