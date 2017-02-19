class Config:
    _instance = None

    def __init__(self):
        self.MAX_TRIES = 1000
        self.SIZE = 0
        self.A = [1][1]

     def getInstance(self):
        if self._instance is None:
            self._instance = Config()
        return self._instance

def main():
    config = Config.getInstance()
    config.SIZE = 10
    config = Config.getInstance()
    print (config.SIZE)
if __name__ == '__main__':
    main()