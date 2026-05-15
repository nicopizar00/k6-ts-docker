FROM node:lts-alpine
WORKDIR /app
COPY src/services/catalog/server.js ./server.js
EXPOSE 3001
CMD ["node", "server.js"]
