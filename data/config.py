from environs import Env

env = Env()
env.read_env()

token = env.str("TOKEN")
code = env.str("CODE")
channel_id = env.str("CHANNEL_ID")
hostc = env.str("PG_HOST")
userc = env.str("PG_USER")
passc = env.str("PG_PASS")