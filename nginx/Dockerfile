FROM nginx:stable

ARG DEBIAN_FRONTEND=noninteractive

ENV LANG C.UTF-8

RUN \
  DEPENDENCIES=' \
    curl \
    git \
    htop \
    locales \
    make \
    sudo \
    vim \
    wget \
  ' \
  && apt-get update -y \
  && apt-get install -y $DEPENDENCIES \
  && apt-get autoremove -y \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/* /usr/share/doc /usr/share/man /usr/share/locale \
  && echo "set mouse-=a" >> /root/.vimrc
