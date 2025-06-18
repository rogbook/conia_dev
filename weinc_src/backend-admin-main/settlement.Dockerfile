FROM conialab/v3api_base:1

WORKDIR /usr/src/app
COPY . /usr/src/app

#RUN pip install --disable-pip-version-check -r requirements.txt

RUN ln -snf /usr/share/zoneinfo/Asia/Seoul /etc/localtime && echo Asia/Seoul > /etc/timezone

ENV PYTHONPATH /usr/src/app

RUN chmod +x ./run_settelment.sh
RUN chmod +x ./run_day_inventory.sh

CMD ["sh", "run_settelment.sh"]

