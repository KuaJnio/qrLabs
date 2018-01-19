FROM resin/rpi-raspbian

RUN apt-get update && apt-get install -y python-pip && pip install Flask && pip install gevent && pip install reportlab

ENTRYPOINT ["/usr/bin/python", "-u", "qrlabs.py"]

WORKDIR /root/qrLabs

COPY source .
