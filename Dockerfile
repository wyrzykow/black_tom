FROM python:3.7.3-slim-stretch

ENTRYPOINT ["./run.sh"]

RUN apt-get update && apt-get install -y git libpq-dev gcc gfortran libmagic-dev && apt-get autoclean && rm -rf /var/lib/apt/lists/*

COPY . /black_tom

RUN pip install numpy && pip install -r /black_tom/requirements.txt

WORKDIR /black_tom
