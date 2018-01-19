import logging
from threading import Lock
import sqlite3

LOGGER = logging.getLogger(__name__)


class DatabaseHandler(object):
    def __init__(self):
        try:
            self.lock = Lock()
            self.connection = sqlite3.connect('courses.db')
            self.create_table()
        except Exception as e:
            LOGGER.error('Error in DatabaseHandler.__init__: '+str(e))

    def create_table(self):
        try:
            self.lock.acquire()
            c = self.connection.cursor()
            c.execute("CREATE TABLE IF NOT EXISTS COURSES (DATE INT, LIEU TEXT, LABO TEXT, COURSIER TEXT, NB_TOTAL INT, SANGUINS INT, AUTRES INT);")
            self.connection.commit()
            self.lock.release()
        except Exception as e:
            LOGGER.error('Error in DatabaseHandler.create_table: '+str(e))

    def insert_course(self, date, lieu, labo, coursier, nb_total, sanguins, autres):
        try:
            self.lock.acquire()
            c = self.connection.cursor()
            c.execute('INSERT INTO matches VALUES (?, ?, ?, ?, ?, ?, ?)', (date, lieu, labo, coursier, nb_total, sanguins, autres))
            self.connection.commit()
            self.lock.release()
        except Exception as e:
            LOGGER.error('Error in DatabaseHandler.insert_course: '+str(e))

    def get_all_courses(self):
        try:
            a = [1516374545, "La Chataigneraie", "OAB", "romain", 10, 7, 3]
            b = [1516374954, "Le Modena", "OAB", "julien", 22, 15, 7]
            data = [a, b]
            return data
        except Exception as e:
            LOGGER.error('Error in DatabaseHandler.get_all_courses: '+str(e))
