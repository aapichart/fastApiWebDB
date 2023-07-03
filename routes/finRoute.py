from fastapi import APIRouter


router3=APIRouter(
    tags=["financeModule"]
)

@router3.get("/financeModule/test")
async def test3():
    return {"username3":"test3"}
