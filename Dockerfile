FROM debian
ENV DEBIAN_FRONTEND=noninteractive PKGNAME=zcash-scale-calc
RUN apt-get -y update && apt-get -y install python python-pip python-dev
RUN pip install 'dimana == 0.1.dev0'
COPY . $PKGNAME
WORKDIR $PKGNAME
RUN pip install .
ENTRYPOINT ["zcash-scale-calc"]
