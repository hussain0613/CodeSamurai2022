from fastapi import APIRouter, HTTPException

from sqlalchemy.orm.session import Session
from sqlalchemy.exc import SQLAlchemyError

from app import sessionMaker

from models.db import model_map

router = APIRouter(prefix="/crud", tags=["general_crud"])

def get_model(model_name: str):
    if model_name in model_map:
        return model_map[model_name]
    else:
        raise HTTPException(
            status_code=404, 
            detail=f"model '{model_name}' does not exist."
        )


@router.post("/create/{model_name}/")
def create(model_name: str, data: dict):
    model = get_model(model_name)

    db_object = model(** data)

    session: Session = sessionMaker()
    
    try:
        session.add(db_object)
        session.commit()
    except SQLAlchemyError as e:
        session.rollback()
        session.close()
        raise HTTPException(400, detail=str(e))
    except Exception as e:
        session.rollback()
        session.close()
        raise e
    
    session.close()
    
    return {"detail": f"{model_name} created succesfully!"}




@router.get("/get/{model_name}/")
def get(model_name: str, pk):
    model = get_model(model_name)
    
    session: Session = sessionMaker()
    db_object = {}
    
    try:
        db_object = session.query(model).get(pk)
    except SQLAlchemyError as e:
        session.rollback()
        session.close()
        raise HTTPException(400, detail=str(e))
    except Exception as e:
        session.rollback()
        session.close()
        raise e
    session.close()
    
    return db_object

@router.post("/get_many/{model_name}/")
def get_multiple(model_name: str, filter: dict, offset: int = 0, limit: int = None):
    model = get_model(model_name)
    
    session: Session = sessionMaker()
    db_objects: list = []
    
    try:
        db_objects = session.query(model).filter_by(** filter).offset(offset).limit(limit).all()
    except SQLAlchemyError as e:
        session.rollback()
        session.close()
        raise HTTPException(400, detail=str(e))
    except Exception as e:
        session.rollback()
        session.close()
        raise e
    
    session.close()
    
    return db_objects


@router.put("/update/{model_name}/")
def update(model_name: str, pk, new_data: dict):
    model = get_model(model_name)
    
    session: Session = sessionMaker()
    db_object = {}
    
    try:
        db_object = session.query(model).get(pk)
        for field in new_data:
            setattr(db_object, field, new_data[field])
        session.commit()
    except SQLAlchemyError as e:
        session.rollback()
        session.close()
        raise HTTPException(400, detail=str(e))
    except Exception as e:
        session.rollback()
        session.close()
        raise e
    
    session.close()
    
    return {"detail": f"{model_name} row updated succesfully!"}

@router.delete("/delete/{model_name}/")
def delete(model_name: str, pk):
    model = get_model(model_name)
    
    session: Session = sessionMaker()
    db_object = {}
    
    try:
        db_object = session.query(model).get(pk)
        session.delete(db_object)
        session.commit()
    except SQLAlchemyError as e:
        session.rollback()
        session.close()
        raise HTTPException(400, detail=str(e))
    except Exception as e:
        session.rollback()
        session.close()
        raise e
    session.close()
    
    return {"detail": f"{model_name} deleted succesfully!"}

