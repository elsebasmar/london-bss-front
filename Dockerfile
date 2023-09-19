FROM python:3.10.6-buster

COPY requirements-dev.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY londonbssfront londonbssfront
COPY saved_models saved_models
COPY data data

COPY setup.py setup.py
RUN pip install .

CMD uvicorn londonbssfront.api.fast:app --host 0.0.0.0 --port $PORT
