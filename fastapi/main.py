from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"status": "FastAPI is running 🚀"}
print("FastAPI is running on http://localhost:8000 🚀")


