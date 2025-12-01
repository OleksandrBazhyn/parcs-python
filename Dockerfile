FROM python:3.10-slim

WORKDIR /parcs

COPY . /parcs

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["bash"]
