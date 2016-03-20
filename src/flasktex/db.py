import sqlite3
from flasktex.config import ft_config_get


def ft_db_init_conn_sqlite(path=None):
    """Connect to sqlite database.

    return a sqlite3.conn object.
    """
    if path is not None:
        db_file = path
    else:
        db_file = ft_config_get('FT_DB_FILE')
    assert db_file is not None and db_file != ''
    conn = sqlite3.connect(ft_config_get('FT_DB_FILE'))
    assert conn is not None
    return conn


def ft_db_close_conn_sqlite(conn):
    """Close sqlite database connection.
    """
    conn.close()
    return True


def ft_db_setup_record_sqlite(texrequest, conn):
    """Setup a new record described by texrequest.

    Will return the id of established record as int.
    """
    import time
    c = None
    try:
        c = conn.cursor()
    except:
        raise
    var_start_time = time.time()
    texrequest.retrieve_id = hash(var_start_time)
    c.execute('INSERT INTO `work` '
              '(retrieve_id, targz_data, entryfile, start_time, status) '
              'VALUES (?, ?, ?, ?, ?)',
              (
                texrequest.retrieve_id,  # FIXME
                sqlite3.Binary(texrequest.targz_data),
                str(texrequest.entryfile),
                str(var_start_time),
                'INIT',
              ))
    fetched_data = c.execute(
            "SELECT (`id`) FROM `work` WHERE `start_time`=?",
            (str(var_start_time),)
            ).fetchall()
    assert isinstance(fetched_data, list)  # TODO: REMOVE IT
    assert len(fetched_data) == 1
    conn.commit()
    return int(str(fetched_data[0][0]))


def ft_db_record_get_status_sqlite(conn, db_id):
    c = conn.cursor()
    result = c.execute(
            "SELECT (`status`) FROM `work` WHERE `id`=?",
            (db_id,)
            ).fetchall()
    assert len(result) == 1
    return str(result[0][0])


def ft_db_record_set_status_sqlite(conn, db_id, status_str):
    c = conn.cursor()
    c.execute("UPDATE `work` SET `status`=? WHERE `id`=?", (status_str, db_id))
    conn.commit()
    return


def ft_db_record_success_sqlite(conn, db_id, log_str, pdf_data):
    import time
    c = conn.cursor()
    c.execute(
            "UPDATE `work` SET "
            "`status`=?,`output`=?,`stop_time`=?,`log`=? "
            "WHERE `id`=?",
            ('SUCCESS', pdf_data, str(time.time()), log_str, int(db_id)))
    conn.commit()
    return


def ft_db_init_conn(path=None):
    """Meta function to init database connection.
    """
    ret_value = None
    if ft_config_get('FT_DB') == 'SQLITE':
        ret_value = ft_db_init_conn_sqlite(path=path)
    else:  # Unsupported Database Type
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


def ft_db_record_set_status(db_object, db_id, status_str, db_type='SQLITE'):
    ret_value = None
    if db_type == 'SQLITE':
        ret_value = ft_db_record_set_status_sqlite(
                db_object, db_id, status_str)
    else:
        raise Exception('ERR_DB_NOT_IMPLEMENTED')

    return ret_value


def ft_db_record_get_status(db_object, db_id, db_type='SQLITE'):
    ret_value = None
    if db_type == 'SQLITE':
        ret_value = ft_db_record_get_status_sqlite(db_object, db_id)
    else:
        raise Exception('ERR_DB_NOT_IMPLEMENTED')

    return ret_value


def ft_db_record_success(
        db_object, db_id, log_str, pdf_data, db_type='SQLITE'):
    ret_value = None
    if db_type == 'SQLITE':
        ret_value = ft_db_record_success_sqlite(
                db_object, db_id, log_str, pdf_data)
    else:
        raise Exception('ERR_DB_NOT_IMPLEMENTED')

    return ret_value
