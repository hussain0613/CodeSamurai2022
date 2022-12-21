import sqlalchemy as sa

from app import Base

class Project(Base):
    __tablename__ = "project"

    project_id = sa.Column(sa.String, primary_key=True)
    
    name = sa.Column(sa.String)
    location = sa.Column(sa.String)
    latitude = sa.Column(sa.Float)
    longitude = sa.Column(sa.Float)
    exec_ = sa.Column("exec", sa.String, sa.ForeignKey("agency.code", ondelete="set null"))
    cost = sa.Column(sa.Float)
    timespan = sa.Column(sa.Float)
    goal = sa.Column(sa.String)
    start_date = sa.Column(sa.Date)
    completion = sa.Column(sa.Float)
    actual_cost = sa.Column(sa.Float)



class Agency(Base):
    __tablename__ = "agency"

    code = sa.Column(sa.String, primary_key=True)
    
    name = sa.Column(sa.String,)
    type_ = sa.Column("type", sa.String)
    description = sa.Column(sa.String)



class Proposal(Base):
    __tablename__ = "proposal"

    project_id = sa.Column(sa.String, primary_key=True)
    
    name = sa.Column(sa.String)
    location = sa.Column(sa.String)
    latitude = sa.Column(sa.Float)
    longitude = sa.Column(sa.Float)
    exec_ = sa.Column("exec", sa.String, sa.ForeignKey(Agency.code, ondelete="set null"))
    cost = sa.Column(sa.Float)
    timespan = sa.Column(sa.Float)
    goal = sa.Column(sa.String)
    proposal_date = sa.Column(sa.Date)



class Constraint(Base):
    __tablename__ = "constraint"

    code = sa.Column(sa.String, primary_key=True)
    
    max_limit = sa.Column(sa.Integer)
    constraint_type = sa.Column(sa.String)



class Component(Base):
    __tablename__ = "component"

    component_id = sa.Column(sa.String, primary_key=True)
    
    project_id = sa.column(sa.String, sa.ForeignKey(Project.project_id, ondelete="set null"))
    executing_agency = sa.Column(sa.String, sa.ForeignKey(Agency.code, ondelete="set null"))
    component_type = sa.Column(sa.String)
    depends_on = sa.Column(sa.String, sa.ForeignKey("component.component_id", ondelete="set null"))
    budget_ratio = sa.Column(sa.Float)



class UserType(Base):
    __tablename__ = "user_type"

    code = sa.Column(sa.String, primary_key=True)
    
    committee = sa.Column(sa.String)
    description = sa.Column(sa.String)



class User(Base):
    __tablename__ = "user"

    uid = sa.Column(sa.String, primary_key=True)
    
    name = sa.Column(sa.String)
    username = sa.Column(sa.String, unique = True)
    email = sa.Column(sa.String, unique = True)
    user_type = sa.Column(sa.String, sa.ForeignKey(UserType.code, ondelete="set null"))
    agency = sa.Column(sa.String, sa.ForeignKey(Agency.code, ondelete="set null"))



class Issue(Base):
    __tablename__ = "issue"

    issue_id = sa.Column(sa.Integer, primary_key=True, autoincrement = True)
    
    uid = sa.Column(sa.String, sa.ForeignKey(User.uid, ondelete="set null"))
    project_id = sa.Column(sa.String, sa.ForeignKey(Project.project_id, ondelete="set null"))
    description = sa.Column(sa.String)
    status = sa.Column(sa.String)


model_map: dict = {
    "project": Project,
    "agency": Agency,
    "proposal": Proposal,
    "constraint": Constraint,
    "component": Component,
    "user_type": UserType,
    "user": User,
    "issue": Issue
}
