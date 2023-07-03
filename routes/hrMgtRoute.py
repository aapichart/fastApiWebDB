from fastapi import APIRouter


router4=APIRouter(
    tags=["hrMgtModule"]
)

@router4.get("/hrMgtModule/test")
async def test4():
    return {"username4":"test4"}
