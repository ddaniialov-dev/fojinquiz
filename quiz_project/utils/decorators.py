import functools

from fastapi_jwt_auth import AuthJWT


class JwtAccessRequired:
    
    def __call__(self, function):
        @functools.wraps(function)
        async def auth_covered_function(*args, **kwargs):
            auth: AuthJWT = kwargs.get('auth')
            auth.jwt_required()
            
            return await function(*args, **kwargs)
        
        return auth_covered_function
