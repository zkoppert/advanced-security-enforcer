FROM python:3.11-slim-buster

WORKDIR /action/workspace
COPY codeql.yml requirements.txt enforcer.py /action/workspace/

RUN python3 -m pip install --no-cache-dir -r requirements.txt \
    && apt-get -y update \
    && apt-get -y install --no-install-recommends git=1:2.47.2-0.2 \
    && rm -rf /var/lib/apt/lists/*

CMD ["/action/workspace/enforcer.py"]
ENTRYPOINT ["python3", "-u"]

# To run ineractive debug on the docker container
# 1. Comment out the above CMD and ENTRYPOINT lines
# 2. Uncomment the ENTRYPOINT line below

#ENTRYPOINT ["bash"]
