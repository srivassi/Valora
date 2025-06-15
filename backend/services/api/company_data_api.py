from fastapi import FastAPI
from backend.services.company_data_store import build_company_data

app = FastAPI()
company_data = build_company_data()

@app.get("/company/{ticker}")
def get_company_data(ticker: str):
    return company_data.get(ticker.upper(), {})

@app.get("/companies")
def get_all_companies():
    return list(company_data.keys())