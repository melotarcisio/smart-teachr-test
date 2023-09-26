from core.auth import get_password_hash
from database import get_db
from core import settings

test_username = settings.TEST_USER
test_hashed_password = get_password_hash(settings.TEST_PASSWORD)

test_user_query = f"""
    INSERT INTO 
        users (username, password) 
    VALUES 
        ('{test_username}', '{test_hashed_password}')
    ON CONFLICT DO NOTHING;
"""

if __name__ == "__main__":
    db = get_db()
    ddl = open("database/ddl.sql", "r", encoding="utf-8").read()

    for query in ddl.split(";"):
        if query.strip():
            db.execute_raw(query)

    db.execute_raw(test_user_query)

    db.close()
