FROM python:3.11

COPY main/storage/dependencies/requirements.txt /app/main/storage/dependencies/requirements.txt
WORKDIR /app  

RUN pip3 install --upgrade pip
RUN pip3 install --no-cache-dir -r ./main/storage/dependencies/requirements.txt

COPY . /app

CMD python3 /app/main/bot.py