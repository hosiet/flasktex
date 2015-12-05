# CONFIG FILE

FT_DB = 'SQLITE'
FT_DB_FILE = '/tmp/flasktex.db'
FT_WORKER = 'xelatex'
FT_TIMEOUT = 60

def ft_config_get(conf_name):
    assert type(conf_name) == str
    assert conf_name[:3] == 'FT_'
    return globals()[conf_name]
