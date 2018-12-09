FROM python:3.7-slim
COPY . /app
ENTRYPOINT python /app/game_summary.py
