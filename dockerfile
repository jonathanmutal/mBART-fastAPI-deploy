FROM nvidia/cuda:11.0.3-devel-ubuntu18.04

RUN apt-get -y update
RUN apt-get install -y python3.6 python3-pip python3-dev python3-setuptools
RUN pip3 install -U pip setuptools

COPY . /api/API_MBART
WORKDIR /api/API_MBART

RUN cd /api/API_MBART
RUN mkdir -p logging
RUN pip3 install -r requeriments.txt

ENV PYTHONPATH=/api/API_MBART

EXPOSE 8000

# uvicorn configuration
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

ENTRYPOINT ["uvicorn"]
CMD ["app:app", "--host", "0.0.0.0", "--port", "8000"]

# if we want to save the intermedate images (debug propouses): set DOCKER_BUILDKIT=0
