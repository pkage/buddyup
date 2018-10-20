import sqlite3
from datetime import datetime

class BuddyUpDB:
    conn = None

    def __init__(self, conn_addr):
        """__init__

        :param conn_addr: Connection address
        """
        self.conn = sqlite3.connect(conn_addr)
        self.conn.row_factor = sqlite3.Row

        self.init_tables(flush=False)

    def init_tables(self, flush=False):
        c = self.conn.cursor()

        if flush:
            c.executescript('''
                DROP TABLE Users;
                DROP TABLE Schedules;
                DROP TABLE Gyms;
            ''')

        c.execute('''
            CREATE TABLE IF NOT EXISTS Users (
                id          INTEGER PRIMARY KEY,
                email       TEXT NOT NULL
            );
        ''')

        c.execute('''
            CREATE TABLE IF NOT EXISTS Schedules (
                id          INTEGER PRIMARY KEY,
                name        INTEGER NOT NULL,
                owner       INTEGER NOT NULL,
                FOREIGN KEY (owner) REFERENCES Users (id)
                    ON DELETE CASCADE ON UPDATE NO ACTION
            );
        ''')
        
        c.execute('''
            CREATE TABLE IF NOT EXISTS UserSchedules (
                id          INTEGER PRIMARY KEY,
                user        INTEGER NOT NULL,
                sched       INTEGER NOT NULL,
                FOREIGN KEY (user) REFERENCES Users (id)
                    ON DELETE CASCADE ON UPDATE NO ACTION,
                FOREIGN KEY (sched) REFERENCES Schedules (id)
                    ON DELETE CASCADE ON UPDATE NO ACTION
            )
        ''')

        c.execute('''

            CREATE TABLE IF NOT EXISTS FreeSlots (
                id          INTEGER PRIMARY KEY,
                sched       INTEGER NOT NULL,
                time_min    INTEGER NOT NULL,
                time_max    INTEGER NOT NULL,
                FOREIGN KEY (sched) REFERENCES Schedules (id)
                    ON DELETE CASCADE ON UPDATE NO ACTION
            )
        ''')

        self.conn.commit()

    def add_user(self, email: str) -> int:
        """
        Add a user

        :param email: email of user
        :type email: str
        :returns: new user id
        :rtype: int
        """

        c = self.conn.cursor()
        c.execute('INSERT INTO Users (email) VALUES (?)', (email,))
        uid = c.lastrowid
        self.conn.commit()
        return uid

    def add_schedule(self, uid: int, name: str) -> int:
        """
        Add schedule

        :param uid: User ID
        :type uid: int
        :param name: Schedule name
        :type name: str
        :returns: new schedule ID
        :rtype: int
        """
        c = self.conn.cursor()
        c.execute('INSERT INTO Schedules (owner, name) VALUES (?,?)', (uid, name))
        uid = c.lastrowid
        self.conn.commit()
        return uid

    def add_user_to_sched(self, uid: int, sched: int) -> None:
        """
        Add user to sched

        :param uid: User ID
        :type uid: int
        :param sched: Schedule ID
        :type sched: int
        :rtype: None
        """
        c = self.conn.cursor()
        c.execute('INSERT INTO UserSchedules (user, sched) VALUES (?,?)', (uid, sched))
        uid = c.lastrowid
        self.conn.commit()
        return uid


    def remove_user(self, uid: int) -> None:
        """
        Remove a user

        :param uid: user id
        :type uid: int
        :rtype: None
        """
        c = self.conn.cursor()
        c.execute('DELETE FROM Users WHERE id=?', (uid,))
        self.conn.commit()

    def add_free_slot(self, sched: int, time_min: datetime, time_max: datetime) -> int:
        """
        Add a free slot

        :param sched: schedule id
        :type sched: int
        :param time_min: start time
        :type time_min: datetime
        :param time_max: end time
        :type time_max: datetime
        :rtype: int
        """
        c = self.conn.cursor()
        start = time_min.total_seconds()
        end = time_max.total_seconds()

        c.execute('INSERT INTO FreeSlots (sched, time_min, time_max) VALUES (?,?,?)', (sched, start, end))
        sid = c.lastrowid

        self.conn.commit()

        return sid

        self.conn.commit()

    def get_owned_scheds(self, uid: int):
        """
        Get scheds owned by user

        :param uid: user id
        :type uid: int
        """
        c = self.conn.cursor()
        c.execute('SELECT (id, name) FROM Schedules WHERE owner=?', (uid,))

        rows = c.fetchall()

        return rows

    def get_all_scheds(self, uid: int):
        """
        Get all scheds a user has been invited to

        :param uid: User ID
        :type uid: int
        """
        c = self.conn.cursor()
        c.execute('''
            SELECT (s.id, s.name) FROM Schedules s, UserSchedules us WHERE us.user=? AND s.id=us.sched
        ''', (uid,))

        rows = c.fetchall()

        return rows

    def get_all_free_slots(self, sched: int):
        """
        Get all free slots

        :param sched: schedule ID
        :type sched: int
        """
        c = self.conn.cursor()
        c.execute('''
            SELECT (id, time_min, time_max) FROM FreeSlots WHERE sched=?
        ''', (uid,))

        rows = c.fetchall()

        return rows
        
