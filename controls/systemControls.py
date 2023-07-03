from fastapi import APIRouter


router6=APIRouter()

@router6.get("/systemModule/test", tags=["systemModule"])
async def test6():
    return {"username6":"test6"}
