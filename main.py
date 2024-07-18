from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routers.sign import sign
from routers.coin import coin
from routers.files import files

app = FastAPI()

# # public폴더를 static으로
# app.mount("/public", StaticFiles(directory="public"), name="public")

app.include_router(sign)
app.include_router(coin) # <- 이 기능 나 왜 넣었냐 ;;
app.include_router(files)



# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="127.0.0.1", port=8000)