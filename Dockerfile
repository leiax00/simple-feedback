FROM node:22-bookworm-slim AS builder

ARG VITE_APP_PREFIX=/
ARG VITE_APP_API_URL=/api

ENV VITE_APP_PREFIX=${VITE_APP_PREFIX}
ENV VITE_APP_API_URL=${VITE_APP_API_URL}

WORKDIR /app
ADD admin /app/admin
RUN cd admin && \
    yarn install --registry=https://registry.npmmirror.com && \
    yarn build

FROM python:3.13.2-slim-bookworm

WORKDIR /app

ADD server /app/server
ADD requirements.txt /app
COPY --from=builder /app/admin/dist /app/admin/dist

RUN pip install -i https://mirrors.aliyun.com/pypi/simple --upgrade pip && \
    pip install -i https://mirrors.aliyun.com/pypi/simple -r requirements.txt

ENTRYPOINT ["python", "-m", "server.main"]