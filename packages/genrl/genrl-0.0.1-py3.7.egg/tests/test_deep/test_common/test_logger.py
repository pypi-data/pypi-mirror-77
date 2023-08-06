import shutil

from genrl.deep.common import Logger


def test_loggers():
    logger = Logger("./logs", formats=["csv", "stdout", "tensorboard"])
    logger.write({"hello": 0000, "Timestep": 10})
    logger.close()
    shutil.rmtree("./logs")
