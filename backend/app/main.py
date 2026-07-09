from fastapi import FastAPI

app = FastAPI(title="VetCare Pro API")


@app.get("/")
def read_root():
    return {"mensaje": "VetCare Pro API funcionando"}