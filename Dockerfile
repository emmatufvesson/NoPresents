FROM python:3.9-slim-bullseye

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    usbutils \
    libusb-1.0-0-dev \
    libjpeg-dev \
    libtiff5-dev \
    libavcodec-dev \
    libavformat-dev \
    libswscale-dev \
    libv4l-dev \
    gnupg \
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
    numpy==1.26.4 \
    opencv-python-headless \
    pillow
# Install pycoral and tflite-runtime from Coral's wheel
RUN pip install --no-cache-dir \
    https://github.com/google-coral/pycoral/releases/download/v2.0.0/pycoral-2.0.0-cp39-cp39-linux_aarch64.whl \
    https://github.com/google-coral/pycoral/releases/download/v2.0.0/tflite_runtime-2.5.0.post1-cp39-cp39-linux_aarch64.whl

# Copy your application code
COPY . /app

CMD ["python", "object_detection.py"]
