from fastapi import FastAPI
from routers import news,users,favorite,history
from fastapi.middleware.cors import CORSMiddleware

from utils.exception_handlers import register_exception_handlers

app = FastAPI()

# 注册异常处理器
register_exception_handlers(app)


app.add_middleware(
    CORSMiddleware,
    allow_origin_regex="http://localhost:\d+",  #允许跨域访问的正则表达式
    allow_credentials=True,                     #允许跨域请求携带cookie
    allow_methods=["*"],                        #允许跨域请求的方法
    allow_headers=["*"],                        #允许跨域请求的header
)

@app.get("/")
async def root():
    return {"message": "Hello World"}


#挂载路由
app.include_router(news.router)
app.include_router(users.router)
app.include_router(favorite.router)
app.include_router(history.router)