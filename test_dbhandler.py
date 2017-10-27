from unittest import TestCase
import os

from sqlalchemy import (create_engine)
from sqlalchemy.orm import (scoped_session, sessionmaker)

from crawler_db import Base


class DBHandler(TestCase):

    def init_engine(self):
        # get database connection URL from DBURL environment variable
        # DBURL="mysql+mysqlconnector://crawler:abc123@localhost"
        url = os.environ['DBURL']
        self.engine = create_engine(url)

        # create distinct database sessions per each test case
        self.Session = scoped_session(sessionmaker())
        self.Session.configure(bind=self.engine)

    def del_engine(self):
        self.Session.remove()
        self.engine.dispose()

    def setup_db(self, dbschema):
        self.engine.execute("CREATE DATABASE IF NOT EXISTS " + dbschema)
        self.engine.execute("USE " + dbschema)

        # clean database
        Base.metadata.drop_all(self.engine)
        Base.metadata.create_all(self.engine)
