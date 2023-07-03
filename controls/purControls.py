from fastapi import APIRouter


router5=APIRouter()

@router5.get("/purchasingModule/test", tags=["purchasingModule"])
async def test5():
    return {"username5":"test5"}
