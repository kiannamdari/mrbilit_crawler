FROM python:3.13.14-trixie
LABEL maintainer="kian namdari"
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-tk \
    && rm -rf /var/lib/apt/lists/*
COPY . .
RUN pip install --no-cache-dir pyyaml aiohttp fake_useragent
CMD ["python3", "flights_ui.py"]
