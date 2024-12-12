PORT="${PORT:-8080}"
uvicorn main:app --port $PORT --host 0.0.0.0 --forwarded-allow-ips '*' --reload
# uvicorn main:app --port 8080 --host 0.0.0.0 --forwarded-allow-ips '*' --reload