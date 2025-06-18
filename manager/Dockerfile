FROM python:3.10

WORKDIR /app

RUN apt-get update && \
    apt-get install -y curl nodejs npm && \
    pip install fastapi uvicorn && \
    npm install -g serve

COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh

EXPOSE 8000 3000

CMD ["bash", "start.sh"]
