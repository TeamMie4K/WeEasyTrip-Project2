FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY algorithm ./algorithm
COPY backend ./backend
COPY frontend ./frontend
COPY data/provinces ./data/provinces
COPY data/provinces.json data/provinces_status.json data/thai_provinces.py data/name_translations.json ./data/
ENV PORT=8000
CMD ["sh", "-c", "uvicorn main:app --app-dir backend --host 0.0.0.0 --port ${PORT}"]
