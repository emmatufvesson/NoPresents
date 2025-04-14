FROM python:3.9-slim-buster

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    usbutils \
    libusb-1.0-0-dev \
    libcamera0 \
    libepoxy0 \
    libjpeg-dev \
    libtiff5-dev \
    libavcodec-dev \
    libavformat-dev \
    libswscale-dev \
    libv4l-dev \
    && rm -rf /var/lib/apt/lists/*

# Add Google Coral repository
RUN echo "deb https://packages.cloud.google.com/apt coral-edgetpu-stable main" > /etc/apt/sources.list.d/coral-edgetpu.list
RUN curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add -

# Install Coral Edge TPU library
RUN apt-get update && apt-get install -y \
    libedgetpu1-std \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir \
    pycoral==2.0.0 \
    tflite-runtime \
    numpy \
    opencv-python-headless \
    pillow \
    picamera2

# Copy your application code
COPY . /app

CMD ["python", "object_detection.py"]
