# syntax=docker/dockerfile:1.6

# ============================================================
# Stage 1 — Builder
# ============================================================
FROM python:3.6-slim AS builder

WORKDIR /app

# ---------------------------
# Install build dependencies
# ---------------------------
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    build-essential wget unzip git curl ca-certificates libmariadb-dev libmariadb-dev-compat && \
    rm -rf /var/lib/apt/lists/*

# ---------------------------
# Install latest Go (1.24.x)
# ---------------------------
RUN GO_TARBALL=$(curl -fsSL https://go.dev/dl/ | grep -Eo 'go1\.24(\.[0-9]+)?\.linux-amd64\.tar\.gz' | head -n 1) && \
    curl -fsSL https://go.dev/dl/${GO_TARBALL} -o /tmp/go.tar.gz && \
    tar -C /usr/local -xzf /tmp/go.tar.gz && \
    rm /tmp/go.tar.gz && \
    ln -s /usr/local/go/bin/go /usr/local/bin/go

# ---------------------------
# Environment setup
# ---------------------------
ENV GOPATH=/root/go \
    PATH="/usr/local/go/bin:/root/go/bin:${PATH}" \
    GO111MODULE=on \
    PYTHONUNBUFFERED=1

# ============================================================
# 🧱 Cacheable layer for Go tools
# ============================================================
COPY go-tools.txt /tmp/go-tools.txt
RUN set -eux; \
    mkdir -p /root/go/bin; \
    cat /tmp/go-tools.txt | xargs -n6 -I{} sh -c 'echo "Installing {}" && cd $(mktemp -d) && go install "{}"'

# ============================================================
# 🧰 Add external Go tools (gobuster, findomain, amass)
# ============================================================
RUN set -eux; \
    mkdir -p ${GOPATH}/bin && cd /tmp && \
    echo "Installing Gobuster..." && \
    wget --quiet https://github.com/OJ/gobuster/releases/download/v3.5.0/gobuster_3.5.0_Linux_x86_64.tar.gz && \
    tar xzf gobuster_3.5.0_Linux_x86_64.tar.gz gobuster -C ${GOPATH}/bin/ && \
    rm gobuster_3.5.0_Linux_x86_64.tar.gz && \
    echo "Installing Findomain..." && \
    wget --quiet https://github.com/Edu4rdSHL/findomain/releases/latest/download/findomain-linux.zip && \
    unzip -j findomain-linux.zip findomain && chmod +x findomain && mv findomain ${GOPATH}/bin/findomain && \
    rm -f findomain-linux.zip && \
    echo "Installing Amass..." && \
    wget --quiet https://github.com/OWASP/Amass/releases/download/v3.19.3/amass_linux_amd64.zip && \
    unzip -j amass_linux_amd64.zip amass_linux_amd64/amass -d ${GOPATH}/bin/ && \
    rm -f amass_linux_amd64.zip

# ============================================================
# Install Python dependencies
# ============================================================
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ============================================================
# Copy app source and collect static files
# ============================================================
COPY . .
RUN mkdir -p logs && chmod 777 logs && python3 manage.py collectstatic --noinput

# ============================================================
# Stage 2 — Runtime
# ============================================================
FROM python:3.6-slim

ENV DEBIAN_FRONTEND=noninteractive
WORKDIR /app

# ---------------------------
# Install runtime dependencies
# ---------------------------
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    mariadb-client libmariadb-dev curl ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# ---------------------------
# Copy from builder
# ---------------------------
COPY --from=builder /usr/local/go /usr/local/go
COPY --from=builder /usr/local/bin /usr/local/bin
COPY --from=builder /usr/local/lib/python3.6 /usr/local/lib/python3.6
COPY --from=builder /root/go /root/go
COPY --from=builder /app /app

# ---------------------------
# Environment setup
# ---------------------------
ENV PATH="/usr/local/go/bin:/root/go/bin:${PATH}" \
    PYTHONUNBUFFERED=1

# ---------------------------
# Expose port
# ---------------------------
EXPOSE 80

# ---------------------------
# Start the application
# ---------------------------
CMD ["sh", "-c", "sleep 2 && \
    python3 manage.py makemigrations && \
    python3 manage.py sqlmigrate Enumeration 0001 && \
    python3 manage.py migrate && \
    gunicorn --bind 0.0.0.0:80 --workers 4 --threads 2 ScanApi.wsgi:application"]
