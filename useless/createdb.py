from data.config import userc, passc, hostc

import psycopg2.extras


async def create_db():
    conn = psycopg2.connect(dbname="postgres", user=userc, password=passc, host=hostc)

    with conn:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            # -----
            try:
                cur.execute("CREATE TABLE admin (code varchar,"
                            "admin_name varchar,"
                            "admin_id varchar,"
                            "text text,"
                            "now_order varchar,"
                            "tele_id varchar);")
            except:
                pass
            # -----
            try:
                cur.execute("CREATE TABLE users (user_id varchar primary key,"
                            "user_name varchar,"
                            "now_order varchar,"
                            "last_order varchar,"
                            "name varchar,"
                            "number varchar,"
                            "places_count integer,"
                            "autos_count integer,"
                            "orders_count integer);")
            except:
                pass
            # -----
            try:
                cur.execute("CREATE TABLE autos (id varchar,"
                            "auto varchar,"
                            "year varchar,"
                            "vin varchar);")
            except:
                pass
            # -----
            try:
                cur.execute("CREATE TABLE places (id varchar,"
                            "place varchar);")
            except:
                pass
            # -----
            try:
                cur.execute("CREATE TABLE orders (id varchar primary key,"
                            "status integer default 0,"
                            "auto varchar,"
                            "year varchar,"
                            "vin varchar,"
                            "photo_tre varchar,"
                            "photo_mar varchar,"
                            "dime_tre integer,"
                            "srok_tre varchar,"
                            "place varchar,"
                            "bonus varchar,"
                            "delete_id integer);")
            except:
                pass
            # -----

    conn.close()
