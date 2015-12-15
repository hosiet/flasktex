import sqlite3

from flasktex.config import ft_config_get

def ft_db_init_conn_sqlite(path:str=None):
    """Connect to sqlite database.

    return a sqlite3.conn object.
    """
    if path != None:
        db_file = path
    else:
        db_file = ft_config_get('FT_DB_FILE')
    assert db_file != None and db_file != ''
    conn = sqlite3.connect(ft_config_get('FT_DB_FILE'))
    assert conn != None
    return conn

def ft_db_close_conn_sqlite(conn):
    """Close sqlite database connection.
    """
    conn.close()
    return True

def ft_db_setup_record_sqlite(texrequest, conn):
    """Setup a new record described by texrequest.

    Will return the id of established record.
    """
    import time
    c = None
    try:
        c = conn.cursor()
    except:
        raise
    c.execute('INSERT INTO `work` (retrieve_id, targz_data, start_time, status) VALUES (?, ?, ?, ?, ?)',
            (
                None, # FIXME
                texrequest.targz_data,
                time.time(),
                'INIT',
            )
        )
    #FIXME: FINISH ID
    return None

def ft_db_init_conn(path:str=None):
    """Meta function to init database connection.
    """
    ret_value = None
    if ft_config_get('FT_DB') == 'SQLITE':
        ret_value = ft_db_init_conn_sqlite(path=path)
    else: # Unsupported Database Type
        raise Exception('ERR_DB_NOT_IMPLEMENTED')

    return ret_value

def ft_db_close_conn(db_object, db_type='SQLITE'):
    """Meta function to close database connection.
    """
    ret_value = None
    if db_type == 'SQLITE':
        ret_value = ft_db_close_conn_sqlite(db_object)
    else:
        raise Exception('ERR_DB_NOT_IMPLEMENTED')

    return ret_value

def ft_db_setup_record(texrequest, db_object, db_type='SQLITE'):
    ret_value = None
    if db_type == 'SQLITE':
        ret_value = ft_db_setup_record_sqlite(texrequest, db_object)
    else:
        raise Exception('ERR_DB_NOT_IMPLEMENTED')

    return ret_value
