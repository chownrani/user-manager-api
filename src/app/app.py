from fastapi import FastAPI

from src.app.routers import auth, users

app = FastAPI(
    title="User Management API",
    description="User management with JWT",
    version="1.0.0",
    contact={"name": "Raniere", "email": "chownrani@proton.me"},
)


app.include_router(auth.router)
app.include_router(users.router)


@app.get("/", tags=["root"])
async def root():
    return {
        "message": "User Manager API",
        "version": "1.0.0",
        "docs": "/docs",
    }


@app.get("/health", tags=["health"])
async def health_check():
    return {"status": "healthy"}
