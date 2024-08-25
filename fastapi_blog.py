from fastapi import FastAPI, UploadFile, File, Form
import uvicorn
from fastapi.responses import HTMLResponse
from fastapi.responses import JSONResponse
from io import BytesIO
from PIL import Image
from datetime import datetime, timedelta
import base64
from openai import OpenAI
from geopy.distance import geodesic

# OpenAI API 키 설정
open_api_key = ""
client = OpenAI(api_key=open_api_key)
app = FastAPI()

@app.post("/generate-blog/")
def generate_blog():
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content":"Please write a blog writing in korean"}, 
        ],
        max_tokens=500,
        stream=False
    )

    return JSONResponse(response.choices[0].message.content)

@app.get("/", response_class=HTMLResponse)
async def main_page():
    return """
    <html>
        <head>
            <title>블로그 게시글 생성기</title>
        </head>
        <body>
            <h1>블로그 게시글 생성기</h1>
            <form action="/generate-blog/" enctype="multipart/form-data" method="post">
                <input type="file" name="file"><br><br>
                <label for="mood">기분:</label>
                <select name="mood">
                    <option value="활기찬">활기찬</option>
                    <option value="우울한">우울한</option>
                    <option value="무던한">무던한</option>
                </select><br><br>
                <label for="tone">말투:</label>
                <select name="tone">
                    <option value="격식있는">격식있는</option>
                    <option value="캐주얼한">캐주얼한</option>
                    <option value="유머러스한">유머러스한</option>
                </select><br><br>
                <input type="submit" value="생성">
            </form>
        </body>
    </html>
    """