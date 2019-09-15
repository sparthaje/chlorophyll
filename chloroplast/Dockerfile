FROM python:3

RUN mkdir /app
WORKDIR /app
COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD [ "python", "./chloroplast.py", "--production", "True"]