## Copy The Stubbed Database File To A Location 
## Accessible to the Notebook
# ! cp ./database.db /home/database.db

## Init the engine
import os
from sqlalchemy import create_engine, Column, String, Integer

## Note, you need to set the database to database.db
database_filename = "database.db"
project_dir = os.path.dirname(os.path.abspath(''))
database_path = "sqlite:///{}".format(os.path.join(project_dir, database_filename))

engine = create_engine(database_path)

## Init a session
from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)
Session.configure(bind=engine)
session = Session()

## Define a model class
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    # Autoincrementing, unique primary key
    id = Column(Integer().with_variant(Integer, "sqlite"), primary_key=True)
    # String Title
    username = Column(String(80), unique=True)
    # the ingredients blob - this stores a lazy json blob
    # the required datatype is [{'color': string, 'name':string, 'parts':number}]
    password =  Column(String(180), nullable=False)

    def __repr__(self):
         return self.username +": "+self.password

User.metadata.create_all(engine)

User.__table__



## Note, set username to "Abe" to fetch the user from the database
db_user = session.query(User).filter_by(username='Abe').first()
print(db_user)

# Adding a new User
session.rollback()

new_user = User(username='James', password='superstrongpassword')
session.add(new_user)
session.commit()

# Fetch a user from the database
db_user = session.query(User).filter_by(username='James').first()
print(db_user)