import secrets
from http import HTTPStatus

import uvicorn
from PIL import Image
from fastapi import FastAPI, HTTPException, UploadFile

from deps import Config, PredictorInstance, S3Client
from schemas import ErrorMessage, Severity, SeverityResponse

app = FastAPI()


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
