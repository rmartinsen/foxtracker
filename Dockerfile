FROM python:3.7-slim
COPY . /app
RUN pip install -r /app/requirements.txt
ENTRYPOINT python /app/game_summary.py
