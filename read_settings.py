
def read(val):
    try:
        from configparser import ConfigParser
    except ImportError:
        from ConfigParser import ConfigParser  # ver. < 3.0

    # instantiate
    config = ConfigParser()

    # parse existing file
    config.read('db_config.ini')

    # read values from a section
    return config.get('DB_SETTINGS', val)
