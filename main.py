from fastapi import FastAPI #import class FastAPI() từ thư viện fastapi
from typing import Optional # thêm thư viện hỗ trợ optional params

app = FastAPI() # gọi constructor và gán vào biến app

# beginning
@app.get("/") #  khai báo phương thức get và url
async def root(): # do dùng ASGI nên ở đây thêm async, nếu bên thứ 3 không hỗ trợ thì bỏ async đi
    return {"message": "Hello World"}

### Path Parameters
@app.get("/items/{item_id}")   # bỏ trong ngoặc nhọn là biến
async def read_item(item_id : int ): # Nếu đúng định dạng sẽ trả giá trị
    return {"item_id": item_id}

### Optional parameters
@app.get("/items_optional/{item_id}")
async def read_item(item_id: str, q: Optional[str] = None):
    '''
    param item_id: format string
    param q: format string, default value: None, Optional: help you find error that happen
    '''
    if q:
        return {"item_id": item_id, "q": q}
    return {"item_id": item_id}

### Thứ tự 
@app.get("/users/me") # <- here
async def read_user_me():
    return {"user_id": "the current user"}

# nếu đảo thứ tự sẽ mất "the current use"
@app.get("/users/{user_id}") # <- and here
async def read_user(user_id: str):
    return {"user_id": user_id}

### PATH IN PATH
@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}


### Query Parameters
fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}] # pair format: key-value

@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit] # trả về dữ liệu từ skip đến skip + limit


### Query parameter type conversion
@app.get("/items_type_conversion/{item_id}")
async def read_item(item_id: str, short: bool = False): # param short với định dạng boolean có giá trị mặc định là False
    item = {"item_id": item_id}
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item
# http://127.0.0.1:8000/items_type_conversion/hellllo?short=True


### Multiple path and query parameters: Các đường dẫn lồng nhau
@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(user_id: int, item_id: str):
    item = {"item_id": item_id, "owner_id": user_id}
    return item
# http://127.0.0.1:8000/users/1/items/helllo

### Required query parameters
@app.get("/items_query/{item_id}")
async def read_user_item(item_id: str):
    try:
        item_id = item_id.split("=")
        item = {"item_id": item_id[0], "needy":  item_id[1]}
    except:
        item = {"item_id": item_id, "needy": None}
    return item
# http://127.0.0.1:8000/items_query/a=3

###