FROM python:3.12-slim

WORKDIR /app

# Install Python dependencies
COPY requirements.txt ./
RUN python -m pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . ./

EXPOSE 5000
ENV PYTHONUNBUFFERED=1

CMD ["python", "app.py"]
