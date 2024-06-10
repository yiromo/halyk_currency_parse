from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from schemas.schema import data, check_url, save_to_database, get_currency_pair
router = APIRouter(
    prefix="/currency",
    tags=["Currency"]
)


@router.get("/test_url")
async def test_url():
    data = await check_url()
    return JSONResponse(content=data)

@router.get("/get_data")
async def get_data():
    data_currency = await data()  
    return JSONResponse(content=data_currency)

@router.get("/update_table/")
async def update_table():
    data_currency = await data() 
    return await save_to_database(data_currency)

@router.get("/usd_kzt/")
async def usd_kzt():
    data_currency = await data()
    await save_to_database(data_currency)
    return await get_currency_pair("USD/KZT")

@router.get("/rub_kzt/")
async def rub_kzt():
    data_currency = await data()
    await save_to_database(data_currency)
    return await get_currency_pair("RUB/KZT")

@router.get("/eur_kzt/")
async def eur_kzt():
    data_currency = await data()
    await save_to_database(data_currency)
    return await get_currency_pair("EUR/KZT")

@router.get("/gbp_kzt/")
async def gbp_kzt():
    data_currency = await data()
    await save_to_database(data_currency)
    return await get_currency_pair("GBP/KZT")