from flask import Blueprint

api_v1 = Blueprint('api_v1', __name__, url_prefix='/v1')

from . import errors
from .views import account, committee, community, feedback_mail, image, news, public_info, votes
