def token_required(f):
    from flask import request, jsonify
    import jwt
    from functools import wraps
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']
    
        if not token:
            return jsonify({'message': 'a valid token is missing'})
        try:
            from app import app
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = 'id'
        except:
            return jsonify({'message': 'token is invalid'})
    
        return f(current_user, *args, **kwargs)
    return decorator
