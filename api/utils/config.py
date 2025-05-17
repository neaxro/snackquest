import os


class Config:
    def __init__(self):
        # Flask app related config
        self.APP_HOST = os.getenv("APP_HOST", "0.0.0.0")
        self.APP_PORT = os.getenv("APP_PORT", 5000)
        self.APP_DEBUG = os.getenv("APP_DEBUG", "True") == "True"
        self.MACHINE_INVENTORY_PATH = os.getenv("MACHINE_INVENTORY_PATH", "api/machines")
        self.TIMEZONE = os.getenv("TIMEZONE", "UTC")
        self.DEBUG_LEVEL = os.getenv("DEBUG_LEVEL", "info")

        # Metrics related config
        self.METRICS_PREFIX = os.getenv("METRICS_PREFIX", "snackquest")
        self.METRICS_APP_NAME = os.getenv("METRICS_APP_NAME", "snackquest")

config = Config()