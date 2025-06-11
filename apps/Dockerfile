ARG DOCKER_PYTHON_VERSION=3.13.4-bookworm

ARG PIP_UV_VERSION=0.7.9
ARG PIP_PLAYWRIGHT_VERSION=1.52.0

FROM python:${DOCKER_PYTHON_VERSION}

# uv
ARG PIP_UV_VERSION
RUN pip install uv==${PIP_UV_VERSION}

# playwright
ARG PIP_PLAYWRIGHT_VERSION
RUN pip install playwright==${PIP_PLAYWRIGHT_VERSION}
RUN playwright install --with-deps

WORKDIR /app/
COPY pyproject.toml uv.lock .python-version /app/
COPY src /app/src
RUN uv sync

ENV PATH=/root/.local/bin:$PATH

ENV PLAYWRIGHT_BROWSERS_PATH=/root/.cache/ms-playwright
ENV PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=false
