# main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database.sqlite import engine
from app.routers import router_user
from app.routers import router_vegetable
from app.routers import router_garden

app = FastAPI()

# CORS 설정 : 주석처리 확인
# origins = ["http://localhost:8000"]
origins = ["http://59.5.235.142:8080"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from app.database.model import Base as UserBase
from app.database.model import Base as VegetableBase
from app.database.model import Base as GardenBase

UserBase.metadata.create_all(bind=engine)
VegetableBase.metadata.create_all(bind=engine)
GardenBase.metadata.create_all(bind=engine)

app.include_router(router_user.router)
app.include_router(router_vegetable.router)
app.include_router(router_garden.router)

# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8080)

if __name__ == '__main__':
    import uvicorn
    from subprocess import Popen

    Popen(['python', '-m', 'https_redirect'])
    uvicorn.run(
        'main:app', host="0.0.0.0", port=8080,
        reload=True, reload_dirs=['html_files'],
        ssl_keyfile='key.pem',
        ssl_certfile='cert.pem'
        )
    

# uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
# uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload --ssl-keyfile=./key.pem --ssl-certfile=./cert.pem