FROM alpine:latest

ADD requirements.txt .

RUN set -eux; \
    apk add ffmpeg py3-pip tor; \
    pip install --break-system-packages -Ur requirements.txt; \
    echo -e "SocksPort 0.0.0.0:9050\nControlPort 9051\nCookieAuthentication 1\nRunAsDaemon 1" > /etc/tor/torrc

ADD src .
ADD entrypoint.sh /

EXPOSE 8000
ENV HOST="0.0.0.0"

ENTRYPOINT ["/entrypoint.sh"]
