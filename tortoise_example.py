from tortoise import Tortoise, fields, run_async
from tortoise.models import Model
import configparser

class Dao:
    def __init__(self):
        run_async(self.init())

    async def init(self):
        properties = configparser.ConfigParser()
        properties.read('./properties.ini')
        config = properties['DB']
        host = config['host']
        user = config['user']
        password = config['password']
        database = config['database']

        # db_url ex) {DB_TYPE}://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}?{PARAM1}=value&{PARAM2}=value
        await Tortoise.init(
            db_url=f'mysql://{user}:{password}@{host}:3306/{database}',
            modules={'models': ['models']}
        )
        # Generate the schema
        # await Tortoise.generate_schemas()

       #  conn = Tortoise.get_connection("default")

        # Consider using execute_query_dict to get return values as a dict


    async def test(self):
        conn = Tortoise.get_connection("default")
        val = await conn.execute_query_dict("SELECT * FROM t_category_cd")
        return val


# run_async is a helper function to run simple async Tortoise scripts.
# run_async(init())