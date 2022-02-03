from data.config import userc, passc, hostc

import psycopg2.extras


async def create_db():
    conn = psycopg2.connect(dbname="postgres", user=userc, password=passc, host=hostc)

    with conn:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            # mainadmin --------------------------------------------------
            try:
                cur.execute("CREATE TABLE mainadmin (main_admin_id varchar,"
                            "main_admin_name varchar,"
                            "add_worker_name varchar,"
                            "code varchar);")
            except:
                pass
            # ------------------------------------------------------------

            # admins -----------------------------------------------------
            try:
                cur.execute("CREATE TABLE admins (admin_num serial,"
                            "admin_id varchar,"
                            "admin_name varchar,"
                            "add_worker_name varchar,"
                            "del_admin_num integer);")
            except:
                pass
            # ------------------------------------------------------------

            # users ------------------------------------------------------
            try:
                cur.execute("CREATE TABLE users (user_id varchar primary key,"
                            "user_num serial,"
                            "user_name varchar,"
                            "orders_count integer default 0,"
                            "now_edit_contact varchar,"
                            "last_enter_contact integer,"
                            "enter_contacts_count integer default 0);")
            except:
                pass
            # ------------------------------------------------------------

            # userscontacts ----------------------------------------------
            try:
                cur.execute("CREATE TABLE userscontacts (user_contact_id varchar,"
                            "info varchar,"
                            "del_user_contact_id varchar);")
            except:
                pass
            # ------------------------------------------------------------

            # contactsoptions --------------------------------------------
            try:
                cur.execute("CREATE TABLE contactsoptions (contact_num serial,"
                            "type varchar,"
                            "del_contact_num integer);")
            except:
                pass
            # ------------------------------------------------------------

            # workers ----------------------------------------------------
            try:
                cur.execute("CREATE TABLE workers (worker_num serial,"
                            "worker_name varchar,"
                            "services varchar default 0,"
                            "del_worker_num integer);")
            except:
                pass
            # ------------------------------------------------------------

            # orders -----------------------------------------------------
            try:
                cur.execute("CREATE TABLE orders (order_id varchar,"
                            "service varchar,"
                            "date varchar,"
                            "time varchar,"
                            "worker varchar,"
                            "del_no_worker integer);")
            except:
                pass
            # ------------------------------------------------------------

            # servicesoptions --------------------------------------------
            try:
                cur.execute("CREATE TABLE servicesoptions (service_num serial,"
                            "type varchar,"
                            "del_service_num integer);")
            except:
                pass
            # ------------------------------------------------------------

            # counters ---------------------------------------------------
            try:
                cur.execute("CREATE TABLE counters (admins_count integer default 0,"
                            "workers_count integer default 0,"
                            "real_services_count integer default 0,"
                            "services_count integer default 0,"
                            "contacts_count integer default 0,"
                            "code varchar);")
            except:
                pass
            # ------------------------------------------------------------

            # options ----------------------------------------------------
            try:
                cur.execute("CREATE TABLE options (work_time_text text,"
                            "hello_text text,"
                            "end_text text,"
                            "code varchar);")
            except:
                pass
            # ------------------------------------------------------------

    conn.close()
