from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from PIL import Image
from copywritingAgent.router import agent_menu,agent_socialMedia,agent_advertising,agent_newsletter
from fastapi import FastAPI, File, UploadFile, HTTPException
import json
import io

app = FastAPI()


@app.post("/menu/")
async def process_menu(goal: str):
    try:
        response = agent_menu(goal)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/socialMedia/")
async def process_socialMedia(goal:str, image: UploadFile = File(...)):
    try:
        request_object_content = await image.read()
        img = Image.open(io.BytesIO(request_object_content))
        response = agent_socialMedia(goal, img)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/advertising/")
async def process_advertising(goal: str,interest: str):
    try:
        response = agent_advertising(goal,interest)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@app.post("/newsletter/")
async def process_newsletter(goal: str):
    try:
        response = agent_newsletter(goal)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))