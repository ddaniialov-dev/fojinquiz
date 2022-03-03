import functools

from fastapi_jwt_auth import AuthJWT


class AuthJWTWrapper:
    
    def __call__(self, function):
        @functools.wraps(function)
        def wrapped(*args, **kwargs):
            auth: AuthJWT = kwargs.get('auth')
            auth.jwt_required()
            
            return function(*args, **kwargs)
        
        return wrapped
