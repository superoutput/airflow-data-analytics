settings = {
    # 'adapter_url': {
    #     'BHQ': 'http://172.21.134.146:2300/',
    #     'BSR': 'http://172.21.133.197:2300/'
    # },
    # 'adapter_url':'http://172.21.134.146:2300/',#TC
    'adapter_url': 'http://172.21.133.197:2300/',  # IM
    'his_mongodb': {
        'uri': True,
        'connection_uri': 'mongodb://0412-HMSGW:m9bP36VNyaZT@prod-mongodb-atlas-shard-00-03-qduxy.mongodb.net:27077'
                          '/arcusairdb?ssl=true&authSource=admin',
        # 'connection_uri': 'mongodb://0412-HMSGW:m9bP36VNyaZT@prod-mongodb-atlas-shard-00-03-qduxy.mongodb.net,'
        #                   'prod-mongodb-atlas-shard-00-00-qduxy.mongodb.net,'
        #                   'prod-mongodb-atlas-shard-00-01-qduxy.mongodb.net,'
        #                   'prod-mongodb-atlas-shard-00-02-qduxy.mongodb.net:27017/?authSource=admin&ssl=true'
        #                   '&readPreference=secondary&readPreferenceTags=nodeType:ANALYTICS',
        'count_timeout': 3000,
        'database': 'arcusairdb',
        'host': ['prod-mongodb-atlas-shard-00-00-qduxy.mongodb.net', 'prod-mongodb-atlas-shard-00-01-qduxy.mongodb.net',
                 'prod-mongodb-atlas-shard-00-02-qduxy.mongodb.net'],
        'port': 27017,
        'username': '0412-HMSGW',
        'password': 'm9bP36VNyaZT',
        'mechanism': 'SCRAM-SHA-1',
        'replica_set': 'Prod-MongoDB-Atlas-shard-0',
        'ssl': True,
        'auth_source': 'admin'
    },
    'rabbitmq_settings': {
        'host': [
            '172.21.131.49'
        ],
        'port': 5672,
        'api_port': 15672,
        'vhost': 'hms',
        'username': 'hmsgateway',
        'password': 'Fxig0H8HMS',
        'check_queue_available_timeout': 3.0
    },
    'redis_setting': {
        'host': '172.21.131.52',
        'port': 1234,
        'password': ''
    }
}
