FROM python:3.12-slim

WORKDIR /store

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8005

CMD ["uvicorn","app.main:app","--reload","--host","0.0.0.0","--port","8005"]