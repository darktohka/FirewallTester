FROM python:rc-alpine

ENV SHELL /bin/sh
ENV LANG C.UTF-8

ENV PYTHONUNBUFFERED 1
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PIP_NO_CACHE_DIR 0

COPY . /srv
WORKDIR /srv

RUN \
# Create user
    addgroup -g 424 -S firewalltester \
    && adduser -u 424 -S firewalltester -G firewalltester \
# Install Python dependencies
    && pip install --no-cache --upgrade -r requirements.txt \
    && chown -R firewalltester:firewalltester . \
# Cleanup
    && rm -rf /tmp/*

USER firewalltester
ENTRYPOINT ["python", "-m", "firewalltester.main"]
