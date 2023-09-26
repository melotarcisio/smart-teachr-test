from database import get_db
from core import settings

test_user_query = f"""
INSERT INTO users (username, password) VALUES ({settings.TEST_USER}, {settings.TEST_PASSWORD})
"""

if __name__ == "__main__":
    db = get_db()
    ddl = open("database/ddl.sql", "r", encoding="utf-8").read()

    for query in ddl.split(";"):
        if query:
            db.execute_raw(query)

    db.execute_raw(test_user_query)

    db.close()
