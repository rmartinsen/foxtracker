FROM python:3.7-slim
COPY . /app
ENTRYPOINT python game_summary.py
