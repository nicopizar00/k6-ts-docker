FROM node:lts-alpine
WORKDIR /app
COPY src/services/orders/package.json ./
RUN npm install --production --no-fund --no-audit
COPY src/services/orders/server.js ./server.js
EXPOSE 3002
CMD ["node", "server.js"]
