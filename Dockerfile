FROM python:3.8
ENV PYTHONUNBUFFERED 1
RUN mkdir -p /usr/src/app/
WORKDIR /usr/src/app/

COPY . /usr/src/app/
RUN pip install --upgrade pip && pip install -r requirements.txt

RUN chmod a+x ./run.sh
ENTRYPOINT ["./run.sh"]