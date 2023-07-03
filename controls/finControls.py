from fastapi import APIRouter


router3=APIRouter()

@router3.get("/financeModule/test", tags=["financeModule"])
async def test3():
    return {"username3":"test3"}
