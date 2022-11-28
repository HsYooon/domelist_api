from tortoise import Tortoise, fields, run_async
from tortoise.models import Model

async def init():
    # db_url 예시 => {DB_TYPE}://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}?{PARAM1}=value&{PARAM2}=value
    await Tortoise.init(
        db_url='',
        modules={'models': ['models']}
    )
    # Generate the schema
    await Tortoise.generate_schemas()

# run_async is a helper function to run simple async Tortoise scripts.
run_async(init())