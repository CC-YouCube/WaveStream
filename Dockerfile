FROM alpine:latest

ADD requirements.txt .

RUN apk add ffmpeg py3-pip; pip install --break-system-packages -Ur requirements.txt

ADD src .

EXPOSE 8000

CMD ["python", "app.py"]
