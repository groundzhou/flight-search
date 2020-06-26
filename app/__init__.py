import os
from flask import Flask, request, render_template


def create_app(test_config=None):
    # create and config the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flight.db'),
        JSON_AS_ASCII=False
    )

    if not test_config:
        # load the instance config, if exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # initialize app with database
    from app import database
    database.init_app(app)

    # a simple page that test api
    @app.route('/')
    @app.route('/api')
    def api():
        urls = []
        for rule in app.url_map.iter_rules():
            if rule.endpoint not in ['static', 'api']:
                urls.append(rule)
        return render_template('api-doc.html', urls=urls)

    # register blueprints
    from .api import flights, cities, destinations, prices
    app.register_blueprint(flights.bp)
    app.register_blueprint(cities.bp)
    app.register_blueprint(destinations.bp)
    app.register_blueprint(prices.bp)

    # 解决跨域问题
    app.after_request(cors)

    return app


def cors(res):
    # 添加允许的请求头，解决跨域问题
    res.headers['Access-Control-Allow-Origin'] = request.headers.get('Origin', default='*')
    res.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    return res
