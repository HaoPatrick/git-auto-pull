# Actually it doesn't work with this project
# since we can not access the file outside the container

FROM ubuntu:latest
MAINTAINER Hao Xiangpeng "haoxiangpeng@hotmail.com"

RUN apt-get update -y
RUN apt-get install -y wget

RUN wget -q -nv -O- http://ftp.ru.debian.org/debian/pool/main/n/netselect/netselect_0.3.ds1-26_amd64.deb > /tmp/netselect_0.3.ds1-26_amd64.deb
RUN dpkg -i /tmp/netselect_0.3.ds1-26_amd64.deb
RUN netselect -s1 -t20 `wget -q -nv -O- https://launchpad.net/ubuntu/+archivemirrors | grep -P -B8 "statusUP|statusSIX" | grep -o -P "(f|ht)tp.*\"" | tr '"\n' '  '` 2>/dev/null | awk '{ print $2 }' > /fastest-mirror
RUN MIRROR=`cat /fastest-mirror` && sed -i "s#http://archive.ubuntu.com/ubuntu/#$MIRROR#g" /etc/apt/sources.list

RUN apt-get update -y
RUN apt-get install -y python3-pip python3-dev build-essential
COPY . /app
WORKDIR /app
RUN pip3 install -i https://mirrors.ustc.edu.cn/pypi/web/simple -r requirements.txt
RUN pip3 install -i https://mirrors.ustc.edu.cn/pypi/web/simple gunicorn

EXPOSE 5000
ENV HOME /webapp

ENTRYPOINT ["gunicorn", "-w", "4", "-b", "127.0.0.1:5000", "server:app"]