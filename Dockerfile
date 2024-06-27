FROM python:3.11-slim

# Install tkinter dependencies
RUN apt-get update && apt-get install -y \
    python3-tk \
    git \
    libzbar0 \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt /app/
COPY MoneroSigner/src/ /app/
COPY src/ /app/

RUN pip install --no-cache-dir -r /app/requirements.txt

CMD ["python", "-m", "xmrsigner"]
