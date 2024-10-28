from fastapi import APIRouter,Form,Depends,HTTPException,status
import schema,oauth2

route = APIRouter(prefix='/auth')

@route.post("")
def login(id: str = Form(...),
                    password: str = Form(...),
                    ):
    if id == '123' and password == 'admin':
        access_token = oauth2.create_token({'user_id':id})
        response = schema.Token(access_token=access_token,token_type='Bearar')
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Could Not validate credentials')
    return response
