from flask import Blueprint, send_file
import json

bp = Blueprint('cities', __name__, url_prefix='/api/cities')


@bp.route('', methods=['GET'])
def get_cities():
    """
    获取城市列表
    :return: json格式城市列表
    """
    return send_file('static/cities.json')
    # with open('/static/cities.json', 'r', encoding='utf-8') as f:
    #     return json.load(f)
