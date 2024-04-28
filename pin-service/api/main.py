from fastapi import FastAPI
from api.routers.maps import router as mapRouter
from api.routers.pins import router as pinRouter
from api.routers.users import router as userRouter

app = FastAPI()
app.include_router(userRouter)
app.include_router(mapRouter)
app.include_router(pinRouter)
