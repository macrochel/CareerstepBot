FROM python:3.11

WORKDIR /app

COPY requirements.txt .
RUN pip3 install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY bot.py .
COPY watchdog_reload.py .

CMD ["python", "watchdog_reload.py"]