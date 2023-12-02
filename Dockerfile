# Base image
FROM python:3.10-slim

# Update/upgrade packages
RUN apt-get update && apt-get upgrade

# Create directory
RUN mkdir /ricardo-influxrelay

# Move to directory
WORKDIR /ricardo-influxrelay

# Copy Python requirements file
COPY ./requirements.txt ./requirements.txt

# Install Python requirements
RUN pip install -r ./requirements.txt

# Copy the remaining files
COPY . .

# Run script
ENTRYPOINT [ "bash", "RicardoInfluxRelay.sh" ]
