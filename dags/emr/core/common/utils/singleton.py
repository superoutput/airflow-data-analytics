class SingletonMetaClass(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(cls.__class__, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
