from redis import Redis

class RedisConnect:
	
	def __init__(self):
		# host = huicongSpider.config.redis_config.host
		# port = huicongSpider.config.redis_config.port
		# db = huicongSpider.config.redis_config.db
		host = "127.0.0.1"
		port = 6379
		db = 2
		self.redisConn = Redis(host,port,db)

	def sadd(self,db_name,*obj):
		self.redisConn.sadd(db_name,*obj)

	def sismember(self,db_name,obj):
		return self.redisConn.sismember(db_name,obj)

	def scard(self,db_name):
		return self.redisConn.scard(db_name)

	def pop(self,db_name):
		return self.redisConn.spop(db_name)

