FROM node:20-alpine AS build
WORKDIR /app
COPY package.json package-lock.json* ./
RUN npm install
COPY . .
ARG VITE_API_BASE_URL=
ARG VITE_GRAFANA_URL=http://localhost:3000
ARG VITE_ADMIN_API_TOKEN=
ARG VITE_DEMO_MODE=true
ENV VITE_API_BASE_URL=$VITE_API_BASE_URL \
    VITE_GRAFANA_URL=$VITE_GRAFANA_URL \
    VITE_ADMIN_API_TOKEN=$VITE_ADMIN_API_TOKEN \
    VITE_DEMO_MODE=$VITE_DEMO_MODE
RUN npm run build

FROM nginx:1.27-alpine
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
HEALTHCHECK --interval=10s --timeout=5s --retries=5 CMD wget -qO- http://127.0.0.1/ || exit 1
