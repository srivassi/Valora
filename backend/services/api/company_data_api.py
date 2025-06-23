from fastapi import APIRouter
from ..company_data_store import build_company_data

router = APIRouter()
company_data = build_company_data()

@router.get("/company/{ticker}")
def get_company_data(ticker: str):
    return company_data.get(ticker.upper(), {})

@router.get("/companies")
def get_all_companies():
    return list(company_data.keys())

@router.get("/company/{ticker}/financials")
def get_company_financials(ticker: str):
    return company_data.get(ticker.upper(), {}).get("financials", [])

@router.get("/company/{ticker}/taapi")
def get_company_taapi(ticker: str):
    return company_data.get(ticker.upper(), {}).get("taapi", {})

@router.get("/company/{ticker}/stock_data")
def get_company_stock_data(ticker: str):
    return company_data.get(ticker.upper(), {}).get("stock_data", [])

@router.get("/company/{ticker}/historical_features")
def get_company_historical_features(ticker: str):
    return company_data.get(ticker.upper(), {}).get("historical_features", [])

@router.get("/company/{ticker}/data_types")
def get_company_data_types(ticker: str):
    return list(company_data.get(ticker.upper(), {}).keys())