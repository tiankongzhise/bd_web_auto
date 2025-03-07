import tomllib
import os

if __name__ == '__main__':
    config_path = os.path.abspath('config.toml')
    with open(config_path, "rb") as f:
            config = tomllib.load(f)
    print([config['user_map']['金蛛-新账户4']])