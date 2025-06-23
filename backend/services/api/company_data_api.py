from fastapi import APIRouter
from ..company_data_store import build_company_data
import math

router = APIRouter()

# ✅ Build company data once during startup
company_data = build_company_data()

# ✅ Utility to clean NaN and Infinity values for JSON serialization
def clean_nan_values(obj):
    if isinstance(obj, dict):
        return {k: clean_nan_values(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [clean_nan_values(x) for x in obj]
    elif isinstance(obj, float) and (math.isnan(obj) or math.isinf(obj)):
        return None
    return obj

@router.get("/company/{ticker}")
def get_company_data(ticker: str):
    return clean_nan_values(company_data.get(ticker.upper(), {}))

@router.get("/companies")
def get_all_companies():
    return list(company_data.keys())

@router.get("/company/{ticker}/financials")
def get_company_financials(ticker: str):
    return clean_nan_values(company_data.get(ticker.upper(), {}).get("financials", []))

@router.get("/company/{ticker}/taapi")
def get_company_taapi(ticker: str):
    return clean_nan_values(company_data.get(ticker.upper(), {}).get("taapi", {}))

@router.get("/company/{ticker}/stock_data")
def get_company_stock_data(ticker: str):
    return clean_nan_values(company_data.get(ticker.upper(), {}).get("stock_data", []))

@router.get("/company/{ticker}/historical_features")
def get_company_historical_features(ticker: str):
    return clean_nan_values(company_data.get(ticker.upper(), {}).get("historical_features", []))

@router.get("/company/{ticker}/data_types")
def get_company_data_types(ticker: str):
    return list(company_data.get(ticker.upper(), {}).keys())
