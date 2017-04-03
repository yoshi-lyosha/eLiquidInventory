from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
flavors = Table('flavors', post_meta,
    Column('user_id', Integer),
    Column('flavor_id', Integer),
)

flavor = Table('flavor', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('flavor_name', VARCHAR(length=140)),
)

flavor = Table('flavor', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String),
)

user = Table('user', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('nickname', VARCHAR(length=64)),
    Column('flavor_id', VARCHAR(length=64)),
)

user = Table('user', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['flavors'].create()
    pre_meta.tables['flavor'].columns['flavor_name'].drop()
    post_meta.tables['flavor'].columns['name'].create()
    pre_meta.tables['user'].columns['flavor_id'].drop()
    pre_meta.tables['user'].columns['nickname'].drop()
    post_meta.tables['user'].columns['name'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['flavors'].drop()
    pre_meta.tables['flavor'].columns['flavor_name'].create()
    post_meta.tables['flavor'].columns['name'].drop()
    pre_meta.tables['user'].columns['flavor_id'].create()
    pre_meta.tables['user'].columns['nickname'].create()
    post_meta.tables['user'].columns['name'].drop()
