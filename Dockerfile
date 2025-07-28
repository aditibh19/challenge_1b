FROM python:3.10-slim

WORKDIR /app

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# 1. System dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    fonts-dejavu-core \
 && rm -rf /var/lib/apt/lists/*

# 2. Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir --prefer-binary --default-timeout=180 \
        -r requirements.txt && \
    pip install --no-cache-dir huggingface-hub

# 3. Copy source code (model is NOT included)
COPY . .

# 4. Entrypoint
CMD ["python", "persona_extract.py"]
