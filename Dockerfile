###########################
### Build Phase
###########################

# Base Image
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8-slim AS build

# Update OS
RUN apt-get update && apt-get install gnupg2 curl -y
ENV LANG=C.UTF-8 LC_ALL=C.UTF-8 PYTHONUNBUFFERED=1

# Python dependencies
RUN mkdir /svc
COPY . /svc
WORKDIR /svc
RUN pip install wheel && pip wheel -r requirements.txt --wheel-dir=/svc/wheels
WORKDIR /

# Setup Gcloud storage
RUN echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] http://packages.cloud.google.com/apt cloud-sdk main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list && curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key --keyring /usr/share/keyrings/cloud.google.gpg  add - && apt-get update -y && apt-get install google-cloud-sdk -y
COPY ./service-account.json ./service-account.json
ENV GOOGLE_APPLICATION_CREDENTIALS="service-account.json"
RUN gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}

# Copy models
RUN mkdir /ml-models
RUN gsutil -m cp -R gs://entro-ml-models/facebookbart-large-cnn /ml-models


###########################
### Build Phase
###########################

# Base Image
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8-slim

# Environment Config
ENV LANG=C.UTF-8 LC_ALL=C.UTF-8 PYTHONUNBUFFERED=1
ENV PORT 8080

# Copy models, dependencies and code
COPY --from=build /ml-models /ml-models
COPY --from=build /svc /svc
COPY ./app /app


# Install Python Dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --no-index --find-links=/svc/wheels -r requirements.txt
RUN rm requirements.txt
RUN rm -rf /svc