
#!/bin/sh
set -e

INDEX_FILE="/store/artifacts/extensions_info.json"

# wait until index.json exists
while [ ! -f "$INDEX_FILE" ]; do
  echo "Waiting for $INDEX_FILE ..."
  sleep 2
done

echo "$INDEX_FILE found, starting store..."

exec uvicorn app.main:app --host 0.0.0.0 --port 8005