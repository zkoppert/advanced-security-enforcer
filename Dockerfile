FROM python:3.9.7-alpine as base_image

RUN python3 -m pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["python", "enforcer.py"]