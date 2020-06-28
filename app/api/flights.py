from flask import Blueprint, jsonify, request
from app.database import get_db

bp = Blueprint('flights', __name__, url_prefix='/api/flights')


@bp.route('', methods=['GET'])
def get_flights():
    """
    获取航班信息
    :return: 航班信息列表，json格式
    """
    departure = request.args.get('d', 'CTU')
    destination = request.args.get('a', 'SIA')
    date = request.args.get('date', '2020-07-07')
    order = request.args.get('order', 'price')  # price, time, dtime, atime
    order = 'timediff(atime,dtime)' if order == 'time' else order
    airline = request.args.get('airline')
    max_price = request.args.get('max')
    max_price = int(max_price) if max_price else None

    # 直达航班查询
    sql1 = '''SELECT * FROM flight
    WHERE dcity_code = %s AND acity_code = %s AND date(dtime) = %s ORDER BY {};'''.format(order)

    # 拼接航班查询
    sql2 = '''
    SELECT f1.*, f2.*
    FROM
        flight_joint j,
        flight f1,
        flight f2
    WHERE j.dcity_code = %s
        AND j.acity_code = %s
        AND j.ddate = %s
        AND j.flight_1 = f1.id
        AND j.flight_2 = f2.id
    ORDER BY j.price;'''

    sql3 = '''SELECT f1.*, f2.*
FROM flight_joint j,
     flight f1,
     flight f2,
     min_price m
WHERE j.dcity_code = %s
  AND j.acity_code = %s
  AND j.ddate = %s
  AND j.flight_1 = f1.id
  AND j.flight_2 = f2.id
  AND m.dcity_code = %s
  AND m.acity_code = %s
  AND m.ddate = %s
  AND j.price < m.min_price
ORDER BY j.price
LIMIT 5;'''

    result = {}
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute(sql1, (departure, destination, date))
        result['nonstopFlight'] = cursor.fetchall()
        if len(result['nonstopFlight']) <= 5:
            cursor.execute(sql2, (departure, destination, date))
            result['transitFlight'] = cursor.fetchall()

        else:
            cursor.execute(sql3, (departure, destination, date, departure, destination, date))
            result['transitFlight'] = cursor.fetchall()

    time_format = '%Y-%m-%d %H:%M'

    # 航空公司信息
    airlines = []
    for f in result['nonstopFlight']:
        airlines.append(f['airline'])
    for f in result['transitFlight']:
        airlines.append(f['airline'])
        airlines.append(f['f2.airline'])
    result['airlines'] = list(set(airlines))

    if airline:
        airline = airline.split(';')
        result['nonstopFlight'] = [f for f in result['nonstopFlight'] if f['airline'] in airline]
        result['transitFlight'] = [f for f in result['transitFlight']
                                   if f['airline'] in airline and f['f2.airline'] in airline]
    if max_price:
        result['nonstopFlight'] = [f for f in result['nonstopFlight'] if f['price'] <= max_price]
        result['transitFlight'] = [f for f in result['transitFlight'] if f['price'] + f['f2.price'] <= max_price]

    result['transitFlight'] = result['transitFlight'][0:5]  # 最大5个拼接航班

    for r in result['nonstopFlight']:
        r['time'] = str(r['atime'] - r['dtime']).split(':')
        r['atime'] = r['atime'].strftime(time_format)
        r['dtime'] = r['dtime'].strftime(time_format)
    for r in result['transitFlight']:
        r['time'] = str(r['f2.atime'] - r['dtime']).split(':')
        r['stoptime'] = str(r['f2.dtime'] - r['atime']).split(':')
        r['atime'] = r['atime'].strftime(time_format)
        r['dtime'] = r['dtime'].strftime(time_format)
        r['f2.atime'] = r['f2.atime'].strftime(time_format)
        r['f2.dtime'] = r['f2.dtime'].strftime(time_format)

    return jsonify(result)
