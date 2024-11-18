FROM ubuntu:20.04

RUN apt-get update && apt-get install -y --no-install-recommends ffmpeg python3.9 python3-pip

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python3", "bot.py"]
