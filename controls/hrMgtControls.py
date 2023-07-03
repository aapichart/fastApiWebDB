from fastapi import APIRouter


router4=APIRouter()

@router4.get("/hrMgtModule/test", tags=["hrMgtModule"])
async def test4():
    return {"username4":"test4"}
