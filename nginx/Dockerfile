FROM nginx:1.27-alpine
COPY nginx.conf /etc/nginx/nginx.conf
RUN apk add --no-cache curl
EXPOSE 443
HEALTHCHECK --interval=30s --timeout=3s --retries=3 \
  CMD curl -kfsS https://localhost/healthz || exit 1

