FROM python:3.8-slim-buster

COPY requirements.txt enforcer.py ./

RUN python3 -m pip install --no-cache-dir -r requirements.txt \
    && apt-get -y update \
    && apt-get -y install git

CMD ["enforcer.py"]
ENTRYPOINT ["python3"]