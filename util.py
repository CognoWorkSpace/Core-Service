import os
from config import config
from dotenv import load_dotenv


def get_root():
    return os.path.dirname(os.path.abspath(__file__))


def read_file(path):
    with open(path, mode="r", encoding="utf-8") as f:
        return f.read()


def init():
    load_dotenv()


def conf():
    return config
