FROM ubuntu:22.04

# Install python and libreoffice
RUN apt-get update && apt-get install -y libreoffice python3 python3-pip git libjpeg-dev zlib1g-dev poppler-utils

# install unoserver to python that is used by LibreOffice
RUN /usr/bin/python3 -m pip install --user unoserver

# Set working directory to /app
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip3 install -r requirements.txt

# Copy the current directory contents into the container at /app
COPY src /app/src
COPY main.py /app/main.py
COPY docx_config.json /app/docx_config.json

# run interactively
CMD ["/bin/bash"]