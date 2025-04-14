FROM python:3.9-slim-buster

WORKDIR /app

# Install system dependencies, including gnupg for apt-key
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    gnupg \
    usbutils \
    libusb-1.0-0-dev \
    && rm -rf /var/lib/apt/lists/*

# Add Google Coral repository
RUN echo "deb https://packages.cloud.google.com/apt coral-edgetpu-stable main" > /etc/apt/sources.list.d/coral-edgetpu.list
RUN curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add -

# Update packages and install Coral libraries and Picamera2
RUN apt-get update && apt-get install -y \
    libedgetpu1-std \
    python3-picamera2

# Install Python dependencies
RUN pip install --no-cache-dir \
    pycoral==2.0.0 \
    tflite-runtime \
    numpy \
    opencv-python-headless \
    pillow

# Copy your application code
COPY . /app

CMD ["python", "object_detection.py"]
