from data.config import userc, passc, hostc

import psycopg2.extras


async def create_db():
    conn = psycopg2.connect(dbname="postgres", user=userc, password=passc, host=hostc)

    with conn:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            # -----
            try:
                cur.execute("CREATE TABLE workers (id integer default 0,"
                            "tele_id integer default 0,"
                            "worker_name varchar default 0,"
                            "delete_id integer default 0);")
            except:
                pass
            # -----
            try:
                cur.execute("CREATE TABLE notifies (id integer default 0,"
                            "text text default 0,"
                            "year integer default 0,"
                            "month integer default 0,"
                            "day integer default 0,"
                            "hour integer default 0,"
                            "min integer default 0,"
                            "delete_id integer default 0);")
            except:
                pass
            # -----
            try:
                cur.execute("CREATE TABLE admin (id integer default 0,"
                            "code varchar default 0,"
                            "admin_name varchar default 0,"
                            "workers_count integer default 0,"
                            "notifies_count integer default 0,"
                            "edit_notify integer default 0);")
            except:
                pass

    conn.close()
