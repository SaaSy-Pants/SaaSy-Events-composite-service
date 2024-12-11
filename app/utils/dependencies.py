from fastapi import Request, HTTPException

def get_token(request: Request) -> str:
    if not hasattr(request.state, 'token'):
        raise HTTPException(status_code=401, detail="No token found")
    return request.state.token
