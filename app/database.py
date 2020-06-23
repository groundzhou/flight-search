import pymysql
import click
from flask import current_app, g
from flask.cli import with_appcontext


# 获取数据库
def get_db():
    if 'db' not in g:
        g.db = pymysql.connect(
            host=current_app.config['DB_HOST'],
            user=current_app.config['DB_USER'],
            password=current_app.config['DB_PASSWORD'],
            db=current_app.config['DB_NAME'],
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )

    return g.db


# 关闭数据库
def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


# 初始化数据库
def init_db():
    db = get_db()
    with db.cursor() as cursor:
        with current_app.open_resource('../scripts/schema.sql') as f:
            cursor.executemany(f.read().decode('utf8'), [])
    db.commit()


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    app.teardown_appcontext(close_db)
