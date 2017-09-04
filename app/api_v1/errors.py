from app.common.util.restful_util import error_result
from . import api_v1
import jwt
import traceback


@api_v1.errorhandler(404)
def page_not_found(e):
    traceback.print_exc()
    return error_result(str(e)), 404


@api_v1.errorhandler(jwt.InvalidTokenError)
def unauthorized(e):
    return error_result(str(e)), 401


@api_v1.errorhandler(Exception)
@api_v1.errorhandler(500)
def internal_server_error(e):
    traceback.print_exc()
    return error_result(str(e)), 500

