from flask import Blueprint, jsonify
from app.database import get_db

bp = Blueprint('flights', __name__, url_prefix='/api/flights')


@bp.route('/<departure>/<destination>/<date>', methods=['GET'])
def get_flights(departure, destination, date):
    """
    获取航班信息
    :param departure: 出发地
    :param destination: 目的地
    :param date: 日期
    :return: 航班信息列表，json格式
    """
    sql = 'SELECT * FROM flight WHERE dcity_code = %s and acity_code = %s and date(dtime) = %s'
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute(sql, (departure, destination, date))
        result = cursor.fetchall()
    for r in result:
        r['atime'] = r['atime'].strftime("%Y-%m-%d %H:%M:%S")
        r['dtime'] = r['dtime'].strftime("%Y-%m-%d %H:%M:%S")
    return jsonify(result)
