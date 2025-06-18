FROM conialab/v3store_base:2

WORKDIR /usr/src/app
COPY . /usr/src/app

RUN pip install --disable-pip-version-check -r requirements.txt

RUN ln -snf /usr/share/zoneinfo/Asia/Seoul /etc/localtime && echo Asia/Seoul > /etc/timezone

EXPOSE 5003

CMD ["gunicorn", "--preload", "-c", "gunicorn.conf.py", "app.main:create_app()"]

