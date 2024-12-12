import json

from peewee import *
from peewee_migrate import Router
from playhouse.db_url import connect
# from config import SRC_LOG_LEVELS, DATA_DIR, DATABASE_URL, BACKEND_DIR
import os
import logging

log = logging.getLogger(__name__)
# log.setLevel(SRC_LOG_LEVELS["DB"])


class JSONField(TextField):
    def db_value(self, value):
        return json.dumps(value)

    def python_value(self, value):
        if value is not None:
            return json.loads(value)


# Check if the file exists
# if os.path.exists(f"{DATA_DIR}/ollama.db"):
#     # Rename the file
#     os.rename(f"{DATA_DIR}/ollama.db", f"{DATA_DIR}/webui.db")
#     log.info("Database migrated from Ollama-WebUI successfully.")
# else:
#     pass
# BACKEND_DIR = ""

# # pg_db = PostgresqlDatabase('anvilgpt', user='postgres', password='anvilgpt',
# #                            host='localhost', port=5000)
# # http://anvil-postgres.mysql.anvilcloud.rcac.purdue.edu:5432/
# pg_db = PostgresqlDatabase('anvilgpt', user='postgres', password='anvilgpt',
#                            host='ragdb.mysql.anvilcloud.rcac.purdue.edu', port=5432)
# log.info(f"Connected to a {pg_db.__class__.__name__} database.")
# print(f"Connected to a {pg_db.__class__.__name__} database.")
# router = Router(
#     pg_db,
#     # migrate_dir=BACKEND_DIR / "apps" / "webui" / "internal" / "migrations",
#     migrate_dir="C:/Users/athre/Documents/Athreyan/Purdue/Summer/RCAC/Svelte_projects/temp_folder/open-webui/backend/apps/webui/internal/migrations",
#     logger=log,
# )
# router.run()
# pg_db.connect(reuse_if_open=True)
