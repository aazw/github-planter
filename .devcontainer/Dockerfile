# debian version
# 10 (Buster)
# 11 (Bullseye)
# 12 (Bookworm)
# 13 (Trixie)
# 14 (Forky)

# for main image
ARG DOCKER_DEBIAN_VERSION=bookworm

# for builder images
ARG DOCKER_GO_VERSION=1.24.4-bookworm
ARG DOCKER_NODE_VERSION=22.16.0-bookworm
ARG DOCKER_PYTHON_VERSION=3.13-bookworm
ARG DOCKER_JQ_VERSION=1.8.0
ARG DOCKER_YQ_VERSION=4.45.4
ARG DOCKER_TAPLO_VERSION=0.10.0

# for go install
ARG GO_DOCKERFMT_VERSION=v0.3.7
ARG GO_SHFMT_VERSION=v3.11.0
ARG GO_GO_TASK_VERSION=v3.44.0

# for npm tools
ARG NPM_PRETTIER_VERSION=3.5.3
ARG NPM_RENOVATE_VERSION=40.61.2
ARG NPM_CLAUDE_CODE_VERSION=1.0.24
ARG NPM_CCUSAGE_VERSION=0.8.0

# for pip tools
ARG PIP_UV_VERSION=0.7.13
ARG PIP_PLAYWRIGHT_VERSION=1.52.0

# ##########################################################################################
# builder images
# ##########################################################################################

# golang
# https://hub.docker.com/_/golang
FROM golang:${DOCKER_GO_VERSION} AS golang-builder

# dockerfmt
# https://github.com/reteps/dockerfmt
ARG GO_DOCKERFMT_VERSION
RUN go install github.com/reteps/dockerfmt@${GO_DOCKERFMT_VERSION}

# shfmt
# https://github.com/mvdan/sh
ARG GO_SHFMT_VERSION
RUN go install mvdan.cc/sh/v3/cmd/shfmt@${GO_SHFMT_VERSION}

# go-task
# https://github.com/go-task/task
# https://taskfile.dev/
ARG GO_GO_TASK_VERSION
RUN go install github.com/go-task/task/v3/cmd/task@${GO_GO_TASK_VERSION}

# node
# https://hub.docker.com/_/node
# https://note.milldea.com/posts/two-ways-to-install-nodejs-with-fixed-version-in-dockerfile
FROM node:${DOCKER_NODE_VERSION} AS node-builder

# python
# https://hub.docker.com/_/python
FROM python:${DOCKER_PYTHON_VERSION} AS python-builder
RUN mkdir -p /python-install \
    && cp -r /usr/local/bin /python-install/ \
    && cp -r /usr/local/lib /python-install/ \
    && cp -r /usr/local/include /python-install/ \
    && rm -rf /python-install/lib/pkgconfig

# jq
# https://github.com/mikefarah/yq
# https://github.com/jqlang/jq
FROM ghcr.io/jqlang/jq:${DOCKER_JQ_VERSION} AS jq-builder

# yq
# https://github.com/mikefarah/yq
# https://hub.docker.com/r/mikefarah/yq
FROM mikefarah/yq:${DOCKER_YQ_VERSION} AS yq-builder

# taplo
# https://github.com/tamasfe/taplo
# https://taplo.tamasfe.dev/
# https://hub.docker.com/r/tamasfe/taplo
FROM tamasfe/taplo:${DOCKER_TAPLO_VERSION} AS taplo-builder

# ##########################################################################################
# main image
# ##########################################################################################

# debian
# https://hub.docker.com/_/debian
FROM debian:${DOCKER_DEBIAN_VERSION}
ENV DEBIAN_FRONTEND=noninteractive
ENV DEBCONF_NOWARNINGS=yes

# add distribution packages
RUN apt-get update -y && apt-get install -y --no-install-recommends \
    ca-certificates \
    curl \
    wget \
    git \
    nano \
    less

# dockerfmt
# refs above
COPY --from=golang-builder /go/bin/dockerfmt /usr/local/bin/

# shfmt
# refs above
COPY --from=golang-builder /go/bin/shfmt /usr/local/bin/

# go-task
# refs above
COPY --from=golang-builder /go/bin/task /usr/local/bin/

# node
# refs above
COPY --from=node-builder /usr/local/bin/node /usr/local/bin/node
COPY --from=node-builder /usr/local/lib/node_modules /usr/local/lib/node_modules
RUN ln -s /usr/local/bin/node /usr/local/bin/nodejs \
    && ln -s /usr/local/lib/node_modules/npm/bin/npm-cli.js /usr/local/bin/npm \
    && ln -s /usr/local/lib/node_modules/npm/bin/npm-cli.js /usr/local/bin/npx
RUN npm install -g yarn

# python
# refs above
RUN apt-get update -y && apt-get install -y expat
COPY --from=python-builder /python-install/bin/ /usr/local/bin/
COPY --from=python-builder /python-install/lib/ /usr/local/lib/
COPY --from=python-builder /python-install/include/ /usr/local/include/

# jq
# refs above
COPY --from=jq-builder /jq /usr/local/bin/

# yq
# refs above
COPY --from=yq-builder /usr/bin/yq /usr/local/bin/

# taplo
# refs above
COPY --from=taplo-builder /taplo /usr/local/bin/

# prettier
# https://prettier.io/docs/install
ARG NPM_PRETTIER_VERSION
RUN yarn global add prettier@${NPM_PRETTIER_VERSION}

# renovate
# https://github.com/renovatebot/renovate
# https://www.npmjs.com/package/renovate
ARG NPM_RENOVATE_VERSION
RUN yarn global add renovate@${NPM_RENOVATE_VERSION}

# claude-code
# https://github.com/anthropics/claude-code
# https://github.com/anthropics/claude-code/blob/main/.devcontainer/devcontainer.json
# https://github.com/anthropics/claude-code/blob/main/.devcontainer/Dockerfile
# https://github.com/anthropics/claude-code/blob/main/.devcontainer/init-firewall.sh
RUN apt-get update -y && apt-get install -y \
    less \
    git \
    procps \
    sudo \
    fzf \
    zsh \
    man-db \
    unzip \
    gnupg2 \
    gh \
    iptables \
    ipset \
    iproute2 \
    dnsutils \
    aggregate
ARG NPM_CLAUDE_CODE_VERSION
RUN npm install -g @anthropic-ai/claude-code@${NPM_CLAUDE_CODE_VERSION}
ENV DEVCONTAINER=true

## ccusage
# https://github.com/ryoppippi/ccusage
# https://www.npmjs.com/package/ccusage
ARG NPM_CCUSAGE_VERSION
RUN npm install -g ccusage@${NPM_CCUSAGE_VERSION}

# uv
# https://github.com/astral-sh/uv
# https://pypi.org/project/uv/
ARG PIP_UV_VERSION
RUN pip install uv==${PIP_UV_VERSION}

# playwright
# https://github.com/microsoft/playwright-python
# https://pypi.org/project/playwright/
ARG PIP_PLAYWRIGHT_VERSION
RUN pip install playwright==${PIP_PLAYWRIGHT_VERSION}
RUN playwright install --with-deps

# add vscode user
# https://code.visualstudio.com/remote/advancedcontainers/add-nonroot-user#_creating-a-nonroot-user
ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID

RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
    && apt-get update \
    && apt-get install -y sudo \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL >/etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME
USER $USERNAME
