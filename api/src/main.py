import secrets
from http import HTTPStatus

import uvicorn
from PIL import Image
from fastapi import FastAPI, HTTPException, UploadFile
from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)
from fastapi.staticfiles import StaticFiles

from deps import Config, PredictorInstance, S3Client
from schemas import ErrorMessage, Severity, SeverityResponse

app = FastAPI(docs_url=None, redoc_url=None)

app.mount("/static", StaticFiles(directory="/static"), name="static")

@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="/static/swagger-ui-bundle.js",
        swagger_css_url="/static/swagger-ui.css",
    )

@app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
async def swagger_ui_redirect():
    return get_swagger_ui_oauth2_redirect_html()


@app.get("/redoc", include_in_schema=False)
async def redoc_html():
    return get_redoc_html(
        openapi_url=app.openapi_url,
        title=app.title + " - ReDoc",
        redoc_js_url="/static/redoc.standalone.js",
    )


@app.post('/predict', responses={400: {'model': ErrorMessage}})
async def predict_files(
        files: list[UploadFile],
        predictor: PredictorInstance
) -> list[SeverityResponse]:
    response = []
    for file in files:
        try:
            severity = predictor.predict(file.file)
        except Exception as e:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=f'{file.filename}: {str(e)}',
            )
        response.append(
            SeverityResponse(
                filename=file.filename,
                severity=Severity(severity),
            )
        )

    return response


@app.post('/train/{severity}', responses={400: {'model': ErrorMessage}})
async def add_new_data(
        severity: Severity,
        file: UploadFile,
        config: Config,
        s3_client: S3Client,
):
    try:
        img = Image.open(file.file)
    except Exception:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Could not read image',
        )

    extension = img.format.lower()
    name = secrets.token_urlsafe(16)
    key = f'train/{severity.value}{severity.name}/{name}.{extension}'
    file.file.seek(0)
    await s3_client.upload_fileobj(file.file, config.S3_BUCKET, key)
    return {'status': f'Image with severity {severity.value} is uploaded'}


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8080)
