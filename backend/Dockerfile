FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app/ app/
COPY data/vector_store/ data/vector_store/
# Ollama runs on the host, so use host.docker.internal
ENV OLLAMA_HOST=http://host.docker.internal:11434
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
