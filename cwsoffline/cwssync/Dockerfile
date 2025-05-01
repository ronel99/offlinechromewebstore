FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY cwsoffline/cwssync/extension_sync.py .
COPY cwsoffline/cwssync/recommended_extensions.json .

CMD ["python", "extension_sync.py"]