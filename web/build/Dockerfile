FROM node:18.16.0-alpine as build
WORKDIR /app

COPY package.json .
COPY yarn.lock .
RUN npm install -g yarn --registry=https://registry.npmmirror.com && \
    yarn install || npm install
COPY . /app
RUN npm cache clean -f
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
