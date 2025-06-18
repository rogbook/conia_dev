FROM conialab/v3admin_base:7

WORKDIR /app
COPY . /app

RUN npm install

COPY ./public/ckeditor-custom/build /app/node_modules/@ckeditor/ckeditor5-build-classic/build

ENV TZ=Asia/Seoul
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

EXPOSE 5000
CMD ["npm", "run", "dev"]
