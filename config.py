import yaml


class Config(dict):
    def __init__(self, dicts):
        super().__init__(dicts)

    def __getitem__(self, key):
        if key not in self:
            raise Exception("key {} not in available_setting".format(key))
        return super().__getitem__(key)

    def __setitem__(self, key, value):
        if key not in self:
            raise Exception("key {} not in available_setting".format(key))
        return super().__setitem__(key, value)

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError as e:
            return e
        except Exception as e:
            raise e


def transform_keys(data, parent_key=''):
    new_data = {}
    for k, v in data.items():
        new_key = f'{parent_key}_{k}'.upper() if parent_key else k.upper()
        if isinstance(v, dict):
            new_data.update(transform_keys(v, new_key))
        else:
            new_data[new_key] = v
    return new_data


with open('config.yml', 'r') as f:
    yaml_data = yaml.safe_load(f)

conf = Config(transform_keys(yaml_data))
