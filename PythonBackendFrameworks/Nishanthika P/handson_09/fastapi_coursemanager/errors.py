"""
errors.py
Hands-On 8, Task 2, step 85: standardised error response format and a
global exception handler that converts every HTTPException into it.

Format:
{
    "error": {
        "code": "NOT_FOUND",
        "message": "Course with id 99 does not exist",
        "field": null
    }
}
"""
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse

# Map HTTP status codes to a short machine-readable error code
STATUS_TO_CODE = {
    400: 'BAD_REQUEST',
    401: 'UNAUTHORIZED',
    404: 'NOT_FOUND',
    409: 'CONFLICT',
    422: 'UNPROCESSABLE_ENTITY',
}


async def http_exception_handler(request: Request, exc: HTTPException):
    code = STATUS_TO_CODE.get(exc.status_code, 'ERROR')
    return JSONResponse(
        status_code=exc.status_code,
        content={
            'error': {
                'code': code,
                'message': exc.detail,
                'field': None,
            }
        },
    )


def not_found(resource: str, resource_id) -> HTTPException:
    """Helper to raise a consistently worded 404."""
    return HTTPException(
        status_code=404,
        detail=f'{resource} with id {resource_id} does not exist',
    )
