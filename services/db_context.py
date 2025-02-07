

from gino import Gino
from .log import logger
from configs.config import bind, sql_name, user, password, address, port, database
from .service_config import DATABASE_URI


# 全局数据库连接对象
db = Gino()


async def init():
    i_bind = DATABASE_URI if DATABASE_URI else bind
    if not i_bind:
        i_bind = f"{sql_name}://{user}:{password}@{address}:{port}/{database}"
    # print(i_bind)
    try:
        await db.set_bind(i_bind)
        await db.gino.create_all()
        logger.info(f'Database loaded successfully!')
    except Exception as e:
        raise Exception(f'数据库连接错误.... e: {e}')


async def disconnect():
    await db.pop_bind().close()

