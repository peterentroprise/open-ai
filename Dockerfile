FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8-slim

# Update OS
RUN apt-get update && apt-get install libssl-dev libcurl4-openssl-dev python-dev python3-setuptools gnupg2 curl gcc -y
RUN ln -s /run/shm /dev/shm
ENV LANG=C.UTF-8 LC_ALL=C.UTF-8 PYTHONUNBUFFERED=1
WORKDIR /

#gcloud storage
RUN echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] http://packages.cloud.google.com/apt cloud-sdk main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list && curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key --keyring /usr/share/keyrings/cloud.google.gpg  add - && apt-get update -y && apt-get install google-cloud-sdk -y

RUN pip3 uninstall crcmod

RUN pip3 install --no-cache-dir -U crcmod

COPY ./service-account.json ./service-account.json

ENV GOOGLE_APPLICATION_CREDENTIALS="service-account.json"

RUN gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}



# Install Python Dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN rm requirements.txt

# copy models

RUN mkdir /ml-models
RUN gsutil -m cp -R gs://entro-ml-models/gpt2 /ml-models

ENV PORT 8080

COPY ./app /app