from db import get_connection, execute

def insert_seasons(year):
    conn = get_connection()

    sql = ''' INSERT INTO Seasons (year)
        VALUES (%s)  
        ON DUPLICATE KEY UPDATE year = year
        '''
    

    execute(conn, sql, (year,))
    conn.commit()
    conn.close()

insert_seasons(2025)