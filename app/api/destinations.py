from flask import Blueprint, jsonify, request
from app.database import get_db

bp = Blueprint('destinations', __name__, url_prefix='/api/destinations')


@bp.route('', methods=['GET'])
def get_destinations():
    """
    飞去哪，获取目的地
    :return: 目的地json列表
    """
    departure = request.args.get('d', 'CTU')
    date = request.args.get('date', '2020-07-08')

    sql = '''
SELECT m.dcity_code, m.acity_code, c.city_name acity, m.ddate, m.min_price, c.latitude, c.longitude
FROM min_price m,
     (SELECT city_code, city_name, AVG(latitude) latitude, AVG(longitude) longitude
      FROM city_airport
      GROUP BY city_code, city_name) c
where m.dcity_code = %s
  AND m.ddate = %s
  AND m.acity_code = c.city_code
ORDER BY m.min_price;'''

    with get_db().cursor() as cursor:
        cursor.execute(sql, (departure, date))
        result = cursor.fetchall()

    # 格式化日期
    for r in result:
        r['ddate'] = r['ddate'].strftime("%Y-%m-%d")

    return jsonify(result)
