from sqlalchemy import create_engine

from temp_messenger.dependencies.users import User

import yaml
with open('config.yaml', 'r') as config_file:
    config = yaml.load(config_file)

DB_URL = config['DB_URIS']['user_service:Base']
print(DB_URL)

engine = create_engine(
    DB_URL
)

User.metadata.drop_all(engine)
User.metadata.create_all(engine)
