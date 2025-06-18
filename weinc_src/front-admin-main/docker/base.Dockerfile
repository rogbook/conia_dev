FROM node:lts-alpine

WORKDIR /app
COPY package.json /app

RUN npm install

ENV TZ=Asia/Seoul
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
