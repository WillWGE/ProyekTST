from fastapi import APIRouter,Depends,status,HTTPException
import schemas,database,models
import hashing
from sqlalchemy.orm import Session

get_db=database.get_db
router=APIRouter(
    prefix="/user",
    tags=["users"]
)
#create user
@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.ShowUser)
def create_user(request:schemas.User,db:Session=Depends(get_db)):  
        new_user=models.User(name=request.name,email=request.email,password=hashing.Hash.bycrypt(request.password)) 
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
 
#show user
@router.get("/{id}",response_model=schemas.ShowUser)
def get_user(id,db:Session=Depends(get_db)):
        user=db.query(models.User).filter(models.User.id==id).first()
        if not user:
           raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"user dengan id {id} tidak ada")
        return user
        