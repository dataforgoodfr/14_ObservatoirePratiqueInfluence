ARG UV_VERSION=0.9.25

FROM ghcr.io/astral-sh/uv:${UV_VERSION} AS uv-repo
FROM python:3.12 AS builder

ENV UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1 \
    UV_NO_EDITABLE=1 \
    UV_PYTHON=/usr/local/bin/python3.12 \
    UV_FROZEN=1 \
    UV_CACHE_DIR=/tmp/uv_cache

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="$VIRTUAL_ENV/bin:/root/.local/bin/:$PATH"

WORKDIR /opi-api

COPY --from=uv-repo /uv /usr/bin/uv
COPY pyproject.toml README.md uv.lock ./

RUN uv sync --no-dev --no-editable --no-install-project

COPY src ./src
RUN uv sync --no-dev --no-editable

FROM python:3.12-slim AS runtime

ENV PATH="$VIRTUAL_ENV/bin:$PATH"

WORKDIR /opi-api

COPY src ./src
COPY migrations ./migrations
COPY entrypoint.sh entrypoint.sh
COPY --from=builder /opi-api/.venv /opi-api/.venv

# Install golang migrate
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    curl \
    gnupg gnupg2 \
    lsb-release
RUN curl -fsSL https://packagecloud.io/golang-migrate/migrate/gpgkey | gpg --dearmor -o /etc/apt/keyrings/migrate.gpg


RUN mkdir install_tools/ &&\
    cd install_tools/  &&\
    python -c "import urllib.request, pathlib; pathlib.Path('migrate.tar.gz').write_bytes(urllib.request.urlopen('https://github.com/golang-migrate/migrate/releases/download/v4.19.1/migrate.linux-amd64.tar.gz').read())"  &&\
    tar xvzf migrate.tar.gz  &&\
    rm migrate.tar.gz  &&\
    rm -f LICENSE README.md  &&\
    cp migrate ../  &&\
    cd ..  &&\
    rm -rf install_tools/

ENTRYPOINT [ "/bin/bash" , "entrypoint.sh" ]
