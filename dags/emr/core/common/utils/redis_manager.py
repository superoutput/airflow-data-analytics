import redis

class Redis_manager():
    def __init__(self):
        self.host = '172.21.131.58'
        self.port = 6379
        self.password = ''
        # self.r_connection = self.connect_redis()
        self.r_connection = None

    def connect_redis(self):
        r = redis.Redis(self.host, self.port, self.password)
        return r

    def del_connection(self):
        del self.r_connection

    def r_set(self, key, value):
        self.r_connection = self.connect_redis()
        res = self.r_connection.setex(key, value)
        self.del_connection()
        return res

    def r_get(self, key):
        self.r_connection = self.connect_redis()
        res = self.r_connection.get(key)
        self.del_connection()
        return res

    def r_exists(self, key):#0=not_exists, 1=exists
        self.r_connection = self.connect_redis()
        res = self.r_connection.exists(key)
        self.del_connection()
        return res
    
    def r_setex(self, key, time, value):
        self.r_connection = self.connect_redis()
        res = self.r_connection.setex(key, time, value)
        self.del_connection()
        return res

