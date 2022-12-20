import sqlalchemy as sa

from app import Base

class Project(Base):
    __tablename__ = "project"

    project_id = sa.Column(sa.String, primary_key=True)
    
    name = sa.Column(sa.String,)
    location = sa.Column(sa.String)
    latitude = sa.Column(sa.Float)
    longitude = sa.Column(sa.Float)
    exec_ = sa.Column("exec", sa.String)
    cost = sa.Column(sa.Float)
    timespan = sa.Column(sa.Float)
    goal = sa.Column(sa.String)
    start_date = sa.Column(sa.Date)
    completion = sa.Column(sa.Float)
    actual_cost = sa.Column(sa.Float)

