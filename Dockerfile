FROM python:3

COPY requirements.txt enforcer.py ./

RUN python3 -m pip install --no-cache-dir -r requirements.txt

CMD ["enforcer.py"]
ENTRYPOINT ["python3"]