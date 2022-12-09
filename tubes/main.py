
from fastapi import FastAPI
import models
from database import engine
from routers import toko,user,authentication


app=FastAPI(title="Sales Forecasting")

models.Base.metadata.create_all(engine)

app.include_router(authentication.router)
app.include_router(toko.router)
app.include_router(user.router)


@app.get("/")
def welcome():
        return {"message": "Hello, Welcome to my TST project!)"}

 




