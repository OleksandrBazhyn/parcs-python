FROM python:3.10-slim

WORKDIR /parcs

RUN apt-get update && apt-get install -y \
    gcc \
    libc-dev \
    && rm -rf /var/lib/apt/lists/*

COPY . /parcs

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["bash"]