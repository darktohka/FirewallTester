FROM python:alpine

ENV SHELL=/bin/sh \
    LANG=C.UTF-8 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=0

COPY requirements.txt /srv
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

COPY . /srv

USER firewalltester
ENTRYPOINT ["python", "-m", "firewalltester.main"]
