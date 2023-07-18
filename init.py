import os
from config import config
from dotenv import load_dotenv


def init():
    load_dotenv()


def conf():
    return config
