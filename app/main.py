import os

# fast api modules
from fastapi import FastAPI
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

# app specific modules
from app.core.image_processor import process_image
from app.repository.storage import MyStorageBucket
from app.repository.fb import ROOT_DIR

app = FastAPI()


@app.on_event("startup")
def on_startup():
    if "build" not in os.listdir():
        os.mkdir(f"{ROOT_DIR}/build")
    else:
        # TODO: Add implementation
        pass


@app.get("/")
def root():
    return {"home": "Hello World"}


@app.get("/result/{key}")  ##endpoint for uploading file
def get_result(key: str):
    try:
        file_name = MyStorageBucket().get_file(key)
        name, results = process_image(os.path.abspath(file_name))
        MyStorageBucket().delete_tmp(file_name)
        return {"status": True, "name": name, "results": results}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail, "status": False},
    )
