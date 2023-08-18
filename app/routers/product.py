import sys

sys.path.append("..")

from fastapi import Depends, APIRouter, HTTPException, UploadFile, File
import json
from app.database import session, func
from sqlalchemy.orm import Session
from app import models

router = APIRouter(
    prefix="/products",
    tags=["Products"],
    responses={404: {"description": "Not found"}}
)


def get_db():
    db = session()
    yield db


@router.get("")
async def read_all_products(page_num: int = 1, page_size: int = 10, db: Session = Depends(get_db)):
    start = (page_num - 1) * page_size
    end = start + page_size

    data = db.query(models.Product).all()

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


@router.post("/file")
async def create_new_products_by_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename.endswith(".json"):
        raise HTTPException(status_code=400, detail="Only JSON files are allowed.")
    content = await file.read()
    try:
        data = json.loads(content)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON format.")
    try:
        products = data.get("products", [])
        for item in products:
            product_model = models.Product()
            product_model.name = item['name']
            db.add(product_model)
            db.flush()
            product_detail = item.get("contain_articles", [])
            for item_detail in product_detail:
                model_article = db.query(models.Article) \
                    .filter(models.Article.id == item_detail['art_id']) \
                    .first()
                if model_article is None:
                    raise HTTPException(status_code=400,
                                        detail="Error on item " + str(item_detail) + "the art_id number" + str(
                                            item_detail['art_id']) + " do not exist in the database.")
                model_product_detail = models.ProductDetail()
                model_product_detail.product_id = product_model.id
                model_product_detail.article_id = item_detail['art_id']
                model_product_detail.amount_of = item_detail['amount_of']
                db.add(model_product_detail)
                db.commit()
        return {"message": "Data imported successfully."}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error importing data: {str(e)}")


@router.get("/detail/{product_id}")
async def read_product_detail(product_id: int,
                              db: Session = Depends(get_db)):
    product_model = db.query(models.Product) \
        .filter(models.Product.id == product_id) \
        .first()

    if product_model is None:
        raise HTTPException(status_code=404, detail=f"Product ID not found!")

    product_json = {'product': product_model}

    product_detail_model = db.query(models.ProductDetail) \
        .filter(models.ProductDetail.product_id == product_id) \
        .all()

    if product_detail_model is not None:
        product_json['product_article_detail'] = product_detail_model
    else:
        product_json['product_article_detail'] = []

    return product_json


@router.post("/sell/{product_id}")
async def sell_product_by_id(product_id: int,
                              db: Session = Depends(get_db)):
    product_detail_model = db.query(models.ProductDetail) \
        .filter(models.ProductDetail.product_id == product_id) \
        .all()

    for row in product_detail_model:
        product_detail_model = db.query(models.Article) \
            .filter(models.Article.id == row.article_id) \
            .first()
        product_detail_model.stock = int(product_detail_model.stock) - int(row.amount_of)
        db.add(product_detail_model)
        db.commit()

    return {"message": "Product Sold Successfully."}
