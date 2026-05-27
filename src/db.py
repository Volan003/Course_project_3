import psycopg2

def create_database(database_name, params):
    conn = psycopg2.connect(dbname='postgres', **params)
    conn.autocommit = True
    cur = conn.cursor()

    try:
        cur.execute(f'DROP DATABASE IF EXISTS {database_name}')
        cur.execute(f'CREATE DATABASE {database_name}')
    except psycopg2.errors.ObjectInUse:
        cur.execute(f"""
            SELECT pg_terminate_backend(pid)
            FROM pg_stat_activity WHERE datname = '{database_name}' AND pid <> pg_backend_pid();
            """)
        cur.execute(f'DROP DATABASE {database_name}')
        cur.execute(f'CREATE DATABASE {database_name}')
    except psycopg2.errors.InvalidCatalogName:
        cur.execute(f'CREATE DATABASE {database_name}')
    finally:
        cur.close()
        conn.close()
