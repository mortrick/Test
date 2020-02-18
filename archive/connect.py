import psycopg2
from archive.config import config

def connect(sql, withreturn=0):
    conn = None
    try:
        # Read connection parameters
        params = config()

        # Connect to postgres DB
        print("Connecting to the postgres database")
        conn = psycopg2.connect(**params)

        # Create a cursor
        cur = conn.cursor()
        print("Execute SQL statements")
        cur.execute(sql)
        conn.commit()
        if withreturn == 1:
            ans = cur.fetchone()
            return ans
        else:
            ans = cur.fetchone()
            print(ans)
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print("Database connection closed")


# sql = "select 1"
# connect(sql)
