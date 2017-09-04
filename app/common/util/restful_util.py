from flask import jsonify


def success_result(message='Successfully!', **kwargs):
    return jsonify(dict(result='success', message=message, **kwargs))


def error_result(message='Failed!', **kwargs):
    return jsonify(dict(result='error', message=message, **kwargs))


