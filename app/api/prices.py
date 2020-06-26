from flask import Blueprint, jsonify, request
from app.database import get_db

bp = Blueprint('prices', __name__, url_prefix='/api/prices')


@bp.route('', methods=['GET'])
def get_prices():
    """
    获取取几个月内的价格
    :return: 价格json列表
    """
    departure = request.args.get('d', 'CTU')
    destination = request.args.get('a', 'BJS')

    sql = 'SELECT ddate, min_price FROM min_price WHERE dcity_code = %s AND acity_code = %s;'
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute(sql, (departure, destination))
        result = cursor.fetchall()

    # 格式化日期
    for r in result:
        r['ddate'] = r['ddate'].strftime("%Y-%m-%d")

    return jsonify(result)
