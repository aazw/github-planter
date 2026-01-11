FROM jetpackio/devbox:latest AS builder

WORKDIR /code/gitlab-planter
USER root:root
RUN mkdir -p /code/gitlab-planter && chown ${DEVBOX_USER}:${DEVBOX_USER} /code/gitlab-planter
USER ${DEVBOX_USER}:${DEVBOX_USER}

COPY --chown=${DEVBOX_USER}:${DEVBOX_USER} devbox.json devbox.json
COPY --chown=${DEVBOX_USER}:${DEVBOX_USER} devbox.lock devbox.lock
RUN devbox install


FROM aazw/devcontainers-devbox-python:5 AS runtime

USER root
COPY --from=builder /nix/store /nix/store
COPY --from=builder /code/gitlab-planter/.devbox /code/gitlab-planter/.devbox
USER vscode

ENV PATH="/code/gitlab-planter/.devbox/nix/profile/default/bin:${PATH}"

USER root
RUN playwright install --with-deps
RUN mkdir -p /home/vscode/.cache/uv
RUN chown -R vscode:vscode /home/vscode/.cache
USER vscode
