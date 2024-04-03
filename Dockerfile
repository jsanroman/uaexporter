FROM python:3.11-bullseye

WORKDIR /usr/src/uaexporter

COPY requirements.txt ./
RUN pip install --progress-bar off -r requirements.txt

COPY . .

CMD ["./uaexporter"]
