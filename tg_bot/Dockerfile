FROM jgoclawski/wget
ARG model_name=hog_cat_boost_v2.cbm
RUN wget https://storage.yandexcloud.net/tnn-hse-medtech/models/${model_name}

FROM python:3.11-slim
ARG model_name=hog_cat_boost_v2.cbm
WORKDIR /src
COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt
COPY src /src
COPY --from=0 ${model_name} ${model_name}
ENV BOT_MODEL_PATH=${model_name}
CMD ["python", "main.py"]
