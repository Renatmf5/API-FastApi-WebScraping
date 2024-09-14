from fastapi import File, UploadFile, HTTPException
from core.config import settings
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError


# Cliente S3
s3_client = boto3.client('s3')

async def upload_file(file: UploadFile = File(...)):
    try:
        # Upload do arquivo para o bucket S3
        s3_client.upload_fileobj(file.file, settings.BUCKET_NAME , file.filename)
        print(f"Arquivo {file.filename} enviado com sucesso para o bucket {settings.BUCKET_NAME}.")
        return {"message": f"Arquivo {file.filename} enviado com sucesso para o bucket {settings.BUCKET_NAME}."}
    except NoCredentialsError:
        raise HTTPException(status_code=403, detail="Credenciais da AWS não encontradas.")
    except PartialCredentialsError:
        raise HTTPException(status_code=403, detail="Credenciais da AWS incompletas.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
