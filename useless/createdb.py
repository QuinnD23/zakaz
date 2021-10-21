from data.config import userc, passc, hostc

import psycopg2.extras


async def create_db():
    conn = psycopg2.connect(dbname="postgres", user=userc, password=passc, host=hostc)

    with conn:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            # -----
            try:
                cur.execute("CREATE TABLE workers (id integer default 0,"
                            "tele_id varchar default 0,"
                            "worker_name varchar default 0,"
                            "delete_id integer default 0);")
            except:
                pass
            # -----
            try:
                cur.execute("CREATE TABLE notifies (id integer default 0,"
                            "text text default 0,"
                            "year varchar default 0,"
                            "month varchar default 0,"
                            "day varchar default 0,"
                            "hour varchar default 0,"
                            "min varchar default 0,"
                            "members_count integer default 0,"
                            "delete_id integer default 0);")
            except:
                pass
            # -----
            try:
                cur.execute("CREATE TABLE notifiesmembers (id_member varchar default 0,"
                            "member_name varchar default 0,"
                            "delete_id integer default 0);")
            except:
                pass
            # -----
            try:
                cur.execute("CREATE TABLE admin (code varchar,"
                            "admin_name varchar,"
                            "workers_count integer default 0,"
                            "notifies_count integer default 0,"
                            "edit_notify integer default 0);")
            except:
                pass

    conn.close()
