FROM python:3.12-slim

WORKDIR /store

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 8005

ENTRYPOINT ["sh", "/entrypoint.sh"]

#CMD ["uvicorn","app.main:app","--reload","--host","0.0.0.0","--port","8005"]