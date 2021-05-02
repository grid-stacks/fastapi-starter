from fastapi import Header, HTTPException


# This dependency requires a x_token header with each api call
async def get_token_header(x_token: str = Header(...)):
    if x_token != "super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")


# This dependency requires to pass token with each api call
async def get_query_token(token: str):
    if token != "aws_bucket_token":
        raise HTTPException(
            status_code=400, detail="No ASW Bucket token provided")
