from pydantic import BaseModel

from typing import Optional

from datetime import date

class ProjectSchema(BaseModel):
    project_id: str
    
    name: str 
    location: str
    latitude: float
    longitude: float
    exec_: str
    cost: float
    timespan: float
    goal: str
    start_date: Optional[date]
    completion: Optional[float]
    actual_cost: Optional[float]

    class Config:
        orm_mode = True



class AgencySchema(BaseModel):
    code: str
    
    name: str 
    type_: str
    description: str

    class Config:
        orm_mode = True



class ProposalSchema(BaseModel):
    project_id: str
    
    name: str 
    location: str
    latitude: float
    longitude: float
    exec_: str
    cost: float
    timespan: float
    goal: str
    proposal_date: date

    class Config:
        orm_mode = True



class ConstraintSchema(BaseModel):
    code: str
    
    max_limit: int 
    constraint_type: str

    class Config:
        orm_mode = True



class ComponentSchema(BaseModel):
    component_id = str
    
    project_id = str
    executing_agency = str
    component_type = str
    depends_on = str
    budget_ratio = float

    class Config:
        orm_mode = True