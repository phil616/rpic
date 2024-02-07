

class PCPMException(Exception):
    pass

class CryptoException(PCPMException):
    def __init__(self, message, original_exception=None):
        super().__init__(message)
        self.original_exception = original_exception
    pass

class InvalidKeyException(CryptoException):
    pass

class InvalidTypeException(PCPMException):
    pass