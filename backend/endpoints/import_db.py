from fastapi import APIRouter, UploadFile, File, HTTPException

import pandas as pd

from sqlalchemy.dialects.postgresql import insert as pg_insert

from app import engine

from models.db import Project

router = APIRouter(prefix="/import", tags=["import"])


@router.post("/projects/", tags=["project"])
def import_projects(file: UploadFile = File(...)):
    """
    Import customers from a spreadsheet.<br>
    
    There should not be any duplicate rows or any already existing one otherwise the import will fail.<br>
    The columns that are not in the database will be ignored.<br>

    <b>Note</b> Empty i.e. null values will be inserted as null instead of default value.<br>
    """

    projects_df: pd.DataFrame = pd.DataFrame()
    
    if file.filename.endswith('.xlsx'):
        projects_df = pd.read_excel(file.file.read())
    elif file.filename.endswith('.csv'):
        projects_df = pd.read_csv(file.file)
    else:
        raise HTTPException(status_code = 415, detail = "File format not supported, please upload a .csv or .xlsx file")
    

    customers_data: dict = projects_df.astype(object).where(projects_df.notnull(), None).to_dict(orient="records")
    connection = engine.connect()
    transaction = connection.begin()
    try:
        stmt_prod = pg_insert(Project)
        cusor_result = connection.execute(stmt_prod, customers_data)
        transaction.commit()

    except Exception as e:
        transaction.rollback()
        transaction.close()
        connection.close()
        raise e
    
    transaction.close()
    connection.close()

    return {"message": "Successfully imported projects from spreadsheet", "rows_inserted": cusor_result.rowcount}
