import sqlite3
from fastapi import FastAPI
from datetime import datetime
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

origins = [
    "http://localhost:3000",  # React 애플리케이션 등의 프론트엔드 서버 주소
    "http://localhost:8080",  # 다른 포트에서 실행 중인 서비스 주소
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # 허용할 출처 목록
    allow_credentials=True,  # 쿠키를 포함한 요청 허용
    allow_methods=["GET", "POST", "PUT", "DELETE"],  # 허용할 HTTP 메소드
    allow_headers=["X-Requested-With", "Content-Type"],  # 허용할 헤더
)

class Post(BaseModel):
    writer: str
    title: str
    content: str

def cntDB(): 
    con = sqlite3.connect("post.db")
    con.row_factory = sqlite3.Row
    return con

@app.get("/")
async def index():
    return JSONResponse({"msg" : "Hello, World!"})

@app.get("/allMemo")
async def allMemo():
    con = cntDB()
    cur = con.cursor()
    rawMemo = cur.execute("SELECT * FROM post")
    mapMemo = list(map(lambda x:dict(x), rawMemo))
    return JSONResponse(mapMemo)

@app.post("/uploadPost")
def uploadPost(post: Post):
    con = cntDB()
    cur = con.cursor()

    writer = post.writer
    title = post.title
    content = post.content
    
    cur.execute("INSERT INTO post (writer, title, content) VALUES (?, ?, ?)", (writer, title, content))

    con.commit()