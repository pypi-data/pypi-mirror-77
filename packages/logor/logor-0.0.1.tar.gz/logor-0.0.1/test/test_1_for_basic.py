import logor

logger = logor.withFields({
    "FUNC": __name__,
    "ENV": "DEV",
})

logger.info("hello world")
logger.warning("hello world")
logger.error("hello world")

if __name__ == '__main__':
    with logor.Logor(__name__):
        pass
