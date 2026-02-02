# Fase de construcción.
FROM node:lts-alpine as build-stage

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

RUN npm run build

# Fase de ejecución.
FROM node:lts-alpine as production-stage

WORKDIR /app

RUN npm install -g serve

COPY --from=build-stage /app/dist ./dist

EXPOSE 5173

CMD ["serve", "-s", "dist", "-l", "5173"]

