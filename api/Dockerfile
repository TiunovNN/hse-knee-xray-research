FROM jgoclawski/wget
ARG model_name=hog_cat_boost_v3.cbm
RUN wget https://storage.yandexcloud.net/tnn-hse-medtech/models/${model_name}

FROM python:3.11-slim
WORKDIR /src
COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt
COPY src /src
ARG model_name=hog_cat_boost_v3.cbm
COPY --from=0 ${model_name} ${model_name}
ENV API_MODEL_PATH=${model_name}
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
