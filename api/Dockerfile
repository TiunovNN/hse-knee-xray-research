FROM jgoclawski/wget
ARG model_name=yolov8.pt
RUN wget https://storage.yandexcloud.net/tnn-hse-medtech/models/${model_name}
RUN wget https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js
RUN wget https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css
RUN wget https://cdn.jsdelivr.net/npm/redoc@next/bundles/redoc.standalone.js

FROM python:3.11-slim
RUN apt-get update  && apt-get install --no-install-recommends  -y libgl1-mesa-glx libglib2.0-0 && rm -rf /var/lib/apt/lists/*
RUN mkdir /static
COPY --from=0 swagger-ui-bundle.js /static/swagger-ui-bundle.js
COPY --from=0 swagger-ui.css /static/swagger-ui.css
COPY --from=0 redoc.standalone.js /static/redoc.standalone.js
WORKDIR /src
COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir --upgrade -r /requirements.txt
COPY src /src
ARG model_name=yolov8.pt
COPY --from=0 ${model_name} ${model_name}
ENV API_MODEL_PATH=${model_name}
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--proxy-headers", "--port", "80"]
