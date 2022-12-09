from fastapi import APIRouter,Depends,status,HTTPException
import schemas,database,models,oauth2
from typing import List
from sqlalchemy.orm import Session
import pickle
import numpy as np
import sqlite3


get_db=database.get_db

router=APIRouter(
    prefix="/toko",
    tags=["toko"]
)

#open pickle file 
pickle_in=open("predictor.pkl","rb")
model=pickle.load(pickle_in)

#return semua toko
@router.get("/",response_model=List[schemas.showToko])
def all(db:Session = Depends(database.get_db),current_user:schemas.User=Depends(oauth2.get_current_user)):
        toko=db.query(models.toko).all()
        return toko

#buat row toko baru disimpan dalam database
#status code 201, tanda membuat data baru
@router.post("/",status_code=status.HTTP_201_CREATED)
def create(request:schemas.toko,db:Session=Depends(database.get_db),current_user:schemas.User=Depends(oauth2.get_current_user)):
        new_toko=models.toko(nama=request.nama,lokasi=request.lokasi,tv_ad=request.tv_ad,instagram_ad=request.instagram_ad,newspaper_ad=request.newspaper_ad) 
        db.add(new_toko)
        db.commit()
        db.refresh(new_toko)
        return new_toko

#machine learning aspects
#prediksi penjualan barang elektronik berdasarkan data biaya iklan yang ada di tabel toko
@router.get("/predict")
def predict_sales(current_user:schemas.User=Depends(oauth2.get_current_user)):
        connection = sqlite3.connect("app.db")  # connect to DB
        cursor = connection.cursor()  # get a cursor
        cursor.execute("SELECT * FROM toko")  # execute a simple SQL select query
        rows = cursor.fetchall()  # get all the results from the above query
        list=[]
        for i in range(len(rows)):
            tv_ad_cost=rows[i][3]
            ig_ad_cost=rows[i][4]
            newspaper_ad_cost=rows[i][5]
            features= np.array([[tv_ad_cost,ig_ad_cost,newspaper_ad_cost]])
            prediction=model.predict(features)
            list.append(int(prediction))
        return {"Electronic Unit Sales prediction from table" : list}

#machine learning aspects
#prediksi penjualan barang elektronik berdasarkan data biaya iklan yang ada di tabel toko
@router.post("/predict by input",response_model=schemas.prediction)
def predict_sales(request:schemas.atribut,current_user:schemas.User=Depends(oauth2.get_current_user)):
            tv_ad_cost=request.tv_ad
            ig_ad_cost=request.instagram_ad
            newspaper_ad_cost=request.newspaper_ad
            features= np.array([[tv_ad_cost,ig_ad_cost,newspaper_ad_cost]])
            prediction=model.predict(features)
            return {"Prediction based on input " : prediction}


#return toko berdasarkan id
@router.get("/{id}",status_code=200,response_model=schemas.showToko)
def show(id:int,db:Session=Depends(get_db),current_user:schemas.User=Depends(oauth2.get_current_user)):
        toko=db.query(models.toko).filter(models.toko.id==id).first()
        if not toko:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"toko with the id {id} is not available")
        return toko

#delete toko
@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete(id,db:Session=Depends(get_db),current_user:schemas.User=Depends(oauth2.get_current_user)):
        db.query(models.toko).filter(models.toko.id==id).delete(synchronize_session=False)
        db.commit()
        return "done"

#update toko
@router.put("/{id}",status_code=status.HTTP_202_ACCEPTED)
def update(id,request:schemas.toko,db:Session=Depends(get_db),current_user:schemas.User=Depends(oauth2.get_current_user)):
        toko=db.query(models.toko).filter(models.toko.id==id)
        if not toko.first():
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"toko dengan id {id} tidak ditemukan")
        toko.update(request.dict())
        db.commit()
        return 'updated'



# #machine learning aspects
# #prediksi penjualan barang elektronik
# @router.get("/predict")
# def predict_sales(current_user:schemas.User=Depends(oauth2.get_current_user)):
#         connection = sqlite3.connect("app.db")  # connect to DB
#         cursor = connection.cursor()  # get a cursor
#         cursor.execute("SELECT * FROM toko")  # execute a simple SQL select query
#         rows = cursor.fetchall()  # get all the results from the above query
#         list=[]
#         for i in range(len(rows)):
#             tv_ad_cost=rows[i][3]
#             ig_ad_cost=rows[i][4]
#             newspaper_ad_cost=rows[i][5]
#             features= np.array([[tv_ad_cost,ig_ad_cost,newspaper_ad_cost]])
#             prediction=model.predict(features)
#             list.append(int(prediction))
#         return {"Electronic Unit Sales prediction from table" : list}
        

