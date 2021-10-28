FROM ubuntu:20.04

#RUN pip install PyQt5 PyQtWebEngine

# Env vars for the nvidia-container-runtime.
ENV NVIDIA_VISIBLE_DEVICES all
ENV NVIDIA_DRIVER_CAPABILITIES graphics,utility,compute

RUN apt-get update && apt-get install -y -qq --no-install-recommends \
    libglvnd0 \
    libgl1 \
    libglx0 \
    libegl1 \
    libxext6 \
    libx11-6 \
    python3 \
    python3-pyqt5 \
    python3-pyqt5.qtwebengine \
    # Install Qml
    qmlscene \
    qml-module-* \
    python3-pyqt5.qtopengl \
    python3-pyqt5.qtquick \
    # Install Gstreamer
    gstreamer1.0-libav \
    gstreamer1.0-plugins-bad \
    gstreamer1.0-plugins-base \
    gstreamer1.0-plugins-base-apps \
    gstreamer1.0-plugins-good \
    gstreamer1.0-plugins-ugly \
    alsa-base \
    alsa-utils \
    python3-pyqt5.qtmultimedia \
    && rm -rf /var/lib/apt/lists/*
