import sys

sys.path.append("..")

from fastapi import Depends, APIRouter, HTTPException, UploadFile, File
import json
from app.database import session
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import ReturnTypeFromArgs
from app import models


class UnAccent(ReturnTypeFromArgs):
    pass


router = APIRouter(
    prefix="/articles",
    tags=["Articles"],
    responses={404: {"description": "Not found"}}
)


def get_db():
    db = session()
    yield db


@router.get("/article")
async def read_all_articles(page_num: int = 1, page_size: int = 10, db: Session = Depends(get_db)):
    start = (page_num - 1) * page_size
    end = start + page_size
    data = db.query(models.Article).all()
    data_length = len(data)
    if data_length % page_size != 0:
        total_pages = int((data_length / page_size)) + 1
    else:
        total_pages = round(data_length / page_size)

    if data_length != 0:
        response = {
            "total": data_length,
            "page_size": page_size,
            "total_pages": total_pages,
            "current_page": page_num,
            "data": data[start:end],
        }
        return response
    else:
        raise HTTPException(status_code=201, detail="No data found!")


@router.post("/article/upload")
async def update_article_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename.endswith(".json"):
        return {"error": "Only JSON files are allowed."}

    content = await file.read()
    try:
        data = json.loads(content)
        inventory_items = data.get("inventory", [])
        for item in inventory_items:
            item["id"] = item.pop("art_id")
    except json.JSONDecodeError:
        return {"error": "Invalid JSON format."}

    try:
        for item in inventory_items:
            db_item = models.Article(**item)
            db.add(db_item)
        db.commit()
        return {"message": "Data imported successfully."}
    except Exception as e:
        db.rollback()
        return {"error": f"Error importing data: {str(e)}"}
