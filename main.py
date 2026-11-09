from fastapi import FastAPI,Request,Depends,Form
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from database import engine, Base, get_db
import models
from sqlalchemy import text

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)

templates=Jinja2Templates(directory="templates")

@app.get('/')
def home(request : Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )
@app.get("/products")
def view_products(request:Request,db=Depends(get_db)):
    products = db.query(models.Product).all()
    return templates.TemplateResponse(
        request=request,
        name="products.html",
        context={"products":products}
    )
@app.post("/add-product")
def save_product(
    name: str = Form(...),
    price: float = Form(...),
    discount_price: float = Form(None),
    quantity: int = Form(...),
    image: str = Form(None),
    db=Depends(get_db)
):
    new_product = models.Product(
        name=name,
        price=price,
        discount_price=discount_price,
        quantity=quantity,
        image=image
    )
    db.add(new_product)
    db.commit()
    return RedirectResponse(
        url = "/products",
        status_code=303
    )
@app.get("/add-product")
def add_product_page(request:Request):
    return templates.TemplateResponse(
        request=request,
        name="add_product.html",
        context={}
    )
@app.get("/categories")
def view_categories(request:Request,db=Depends(get_db)):
    categories = db.query(models.Category).all()
    return templates.TemplateResponse(
        request=request,
        name="categories.html",
        context={"categories":categories}
    )
@app.get('/products/category/{category_id}')
def products_by_category(
    category_id: int,
    request: Request,
    db=Depends(get_db)
):
    products = db.query(models.Product).filter(models.Product.category_id == category_id).all()
    return templates.TemplateResponse(
        request=request,
        name="products.html",
        context={"products": products}
    )
@app.get('/register')
def register_page(request:Request):
    return templates.TemplateResponse(
        request=request,
        name="register.html",
        context={}
    )
@app.post('/register')
def register_user(
    name:str=Form(...),
    email:str=Form(...),
    password:str=Form(...),
    db=Depends(get_db)
):
    new_user = models.User(
        name=name,
        email=email,
        password=password
    )
    db.add(new_user)
    db.commit()
    return RedirectResponse(
        url='/login',
        status_code=303
    )
@app.get('/login')
def login_page(request:Request):
    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={}
    )
@app.post('/login')
def login_user(
    request:Request,
    email:str=Form(...),
    password:str=Form(...),
    db=Depends(get_db)
):
    user=db.query(models.User).filter(
        models.User.email == email
    ).first()
    if user and user.password == password:
        return RedirectResponse(
            url="/",
            status_code=303
        )
    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={"error":"Invalid email or password"}
    )