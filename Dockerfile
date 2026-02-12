FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    wget \
    git \
    jq \
    vim-tiny \
    build-essential \
    ca-certificates \
    openssh-client \
    unzip \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . .
RUN pip install --no-cache-dir .

EXPOSE 8000

ENTRYPOINT ["open-terminal"]
CMD ["run"]
