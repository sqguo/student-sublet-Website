from flask import redirect, request
from app.ancillary import bp

@bp.before_app_request
def before_request():
    if request.path[-1:] == '/' and len(request.path) > 1:
        return redirect(request.path[:-1])
    pass
