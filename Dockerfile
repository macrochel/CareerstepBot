FROM python:3.11

COPY /requirements.txt /app/requirements.txt 
WORKDIR /app  

RUN pip3 install --upgrade pip
RUN pip3 install --no-cache-dir -r ./requirements.txt

COPY . /app

CMD python3 /app/bot.py