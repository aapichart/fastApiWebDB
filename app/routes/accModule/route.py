from fastapi import APIRouter


router=APIRouter()

@router.get("/accModule/test", tags=["accModule"])
async def test():
    return {"username":"test"}
