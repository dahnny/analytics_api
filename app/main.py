from fastapi import FastAPI
from app.routes import user, auth, sales, expenses, analytics


app = FastAPI(title="Analytics API", version="1.0.0")

@app.get("/")
async def root():
    return {"message": "Hello World. This is an invoice service."}

app.include_router(user.router, prefix="/api/v1", tags=["users"])
app.include_router(auth.router, prefix="/api/v1", tags=["auth"])
app.include_router(sales.router, prefix="/api/v1", tags=["sales"])
app.include_router(expenses.router, prefix="/api/v1", tags=["expenses"])
app.include_router(analytics.router, prefix="/api/v1", tags=["analytics"]) 

