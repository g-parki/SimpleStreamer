FROM python:3.9

WORKDIR /streamer

#Install dependencies for CV
RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY run.py .

COPY ./scripts ./scripts

CMD ["python", "run.py"]

