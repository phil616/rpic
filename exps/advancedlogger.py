import loguru

logger = loguru.logger

logger.add("file_{time}.log", rotation="500 MB")

logger.info("Hello, World!")