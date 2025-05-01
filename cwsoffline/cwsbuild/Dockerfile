FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY cwsoffline/cwsbuild/cwsbuild.py .

CMD ["python", "cwsbuild.py"]