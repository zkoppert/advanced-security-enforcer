FROM python:3.8-slim-buster

WORKDIR /
COPY requirements.txt enforcer.py ./

RUN python3 -m pip install --no-cache-dir -r requirements.txt \
    && apt-get -y update \
    && apt-get -y install --no-install-recommends git=2.20.1 \
    && rm -rf /var/lib/apt/lists/*

CMD ["enforcer.py"]
ENTRYPOINT ["python3"]