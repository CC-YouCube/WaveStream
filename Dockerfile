FROM alpine:latest

RUN apk add ffmpeg py3-pip; pip install --break-system-packages flask yt-dlp

ADD tmp/dfpwm.py .

EXPOSE 8000

CMD ["python", "dfpwm.py"]
