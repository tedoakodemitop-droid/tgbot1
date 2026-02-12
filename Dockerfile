FROM python:3.9-slim
WORKDIR /app
COPY bot.py .
CMD ["python", "bot.py"]
