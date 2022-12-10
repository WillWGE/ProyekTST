import requests
from fastapi import APIRouter

router=APIRouter(
    prefix="/request",
    tags=["Get Data Partner"]
)

#Fungsi untuk mendapatkan JWT token setelah melakukan login dengan data user yang valid  pada API partner(hefin)
def get_JWTtoken():
    url='https://product-demand-prediction.azurewebsites.net/auth/login'
    data={"username":"hefin@mail.com","password":"finfin"}
    response=requests.post(url,data=data)
    json_response=response.json()
    token=str(json_response['access_token'])
    return token

#fungsi get request
def get_request(url:str):
    link=url 
    headers={"Authorization":f'Bearer {get_JWTtoken()}'}
    response=requests.get(link,headers=headers)
    json_response=response.json()
    return json_response

#melakukan get request untuk mengambil data produk partner(hefin)
@router.get("/get_data_hefin")
def get_product_hefin():
    url='https://product-demand-prediction.azurewebsites.net/product/'
    return get_request(url)

