from fastapi import FastAPI, UploadFile, File
from io import StringIO
import requests

app = FastAPI()


@app.post("/upload-csv/")
async def create_upload_file(file: UploadFile = File(...)):
    content = await file.read()
    df = pd.read_csv(StringIO(content.decode('utf-8')))

    for index, row in df.iterrows():
        # Data Processing and Saving to DB
        # Update existing partner or create a new one
        print(row['CNPJ'], row['Razão Social'])

    return {"filename": file.filename}