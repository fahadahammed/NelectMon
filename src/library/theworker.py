#  Copyright (c) Fahad Ahammed 2021.
from run import app
# REDIS_URL = f'redis://{app.config.get("REDIS_HOST")}:{app.config.get("REDIS_PORT")}/{app.config.get("REDIS_WORKER_DB")}'

# You can also specify the Redis DB to use
REDIS_HOST = app.config.get("REDIS_HOST")
REDIS_PORT = int(app.config.get("REDIS_PORT"))
REDIS_DB = app.config.get("REDIS_WORKER_DB")
# REDIS_PASSWORD = 'very secret'

# Queues to listen on
# QUEUES = ['high', 'default', 'low']

# If you're using Sentry to collect your runtime exceptions, you can use this
# to configure RQ for it in a single step
# The 'sync+' prefix is required for raven: https://github.com/nvie/rq/issues/350#issuecomment-43592410
# SENTRY_DSN = 'sync+http://public:secret@example.com/1'

# If you want custom worker name
# NAME = 'theworker'