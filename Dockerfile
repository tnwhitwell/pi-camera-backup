FROM raspbian/stretch:041518

ENV DEBIAN_FRONTEND noninteractive
RUN apt-get -y update \
    && apt-get -y install \
        python3 \
        python3-pip \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

ADD requirements.txt /app/

ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8

RUN pip3 install -r requirements.txt

RUN wget -qO- https://glare.now.sh/filebrowser/filebrowser/armv7 |\
    tar -C /usr/bin/ -xzf - filebrowser \
    && chmod +x /usr/bin/filebrowser

RUN mkdir /mnt/source /mnt/dest \
    && touch /mnt/source/ABEDF0E7-ECDC-4858-B86E-F4D0E43DED21 \
    && touch /mnt/dest/70212024-D341-4D10-A258-1B8C1A73EC26


VOLUME [ "/app" ]
