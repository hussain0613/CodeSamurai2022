from fastapi import APIRouter, UploadFile, File, HTTPException, Depends

import pandas as pd

from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.exc import IntegrityError

from app import engine
from auth_utils import auth_dependency_factory
from models.db import model_map

router = APIRouter(prefix="/import", tags=["import"])


@router.post("/import_from_spreadsheet/")
def import_from_spreadsheet(model_name: str, file: UploadFile = File(...), _ = Depends(auth_dependency_factory(["SYSADMIN"]))):
    """
    Import data from a spreadsheet.<br>
    
    There should not be any duplicate rows or any already existing one otherwise the import will fail.<br>
    The columns that are not in the database will be ignored.<br>

    <b>Note</b> Empty i.e. null values will be inserted as null instead of default value.<br>
    """

    if model_name not in model_map:
        raise HTTPException(status_code=404, detail=f"Model '{model_name} not found.")

    df: pd.DataFrame = pd.DataFrame()
    
    if file.filename.endswith('.xlsx'):
        df = pd.read_excel(file.file.read())
    elif file.filename.endswith('.csv'):
        df = pd.read_csv(file.file)
    else:
        raise HTTPException(status_code = 415, detail = "File format not supported, please upload a .csv or .xlsx file")
    

    data: dict = df.astype(object).where(df.notnull(), None).to_dict(orient="records")
    connection = engine.connect()
    transaction = connection.begin()
    try:
        stmt_prod = pg_insert(model_map[model_name])
        cusor_result = connection.execute(stmt_prod, data)
        transaction.commit()
    except IntegrityError as e:
        transaction.rollback()
        transaction.close()
        connection.close()
        raise HTTPException(400, detail = str(e))

    except Exception as e:
        transaction.rollback()
        transaction.close()
        connection.close()
        raise e
    
    transaction.close()
    connection.close()

    return {"message": f"Successfully imported to {model_name} from spreadsheet", "rows_inserted": cusor_result.rowcount}