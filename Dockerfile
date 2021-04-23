FROM python:3.8.9-alpine

WORKDIR /root
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY app app
RUN python -m compileall

EXPOSE 8080

WORKDIR /root/app
ENTRYPOINT ["functions-framework"]
