FROM registry-1.docker.io/library/node:lts-trixie-slim as build
COPY games-ui/ app/
WORKDIR /app
RUN yarn install
RUN yarn build


FROM registry-1.docker.io/library/nginx:1.31.7-alpine
WORKDIR /app
COPY --from=build /app/dist .
COPY games-ui/nginx.conf /etc/nginx/nginx.conf
