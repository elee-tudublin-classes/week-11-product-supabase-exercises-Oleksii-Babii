from typing import Annotated
from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

# import service functions
from app.services.product_service import *
from app.services.category_service import getAllCategories

from app.models.product import Product

router = APIRouter()

# set location for templates
templates = Jinja2Templates(directory="app/view_templates")

# handle http get requests for the site root /
# return the todos page
@router.get("/", response_class=HTMLResponse)
async def getProducts(request: Request):

    products = getAllProducts()
    categories = getAllCategories()

    # note passing of parameters to the page
    return templates.TemplateResponse("product/products.html", {"request": request, "products": products, "categories": categories })

@router.get("/update/{id}", response_class=HTMLResponse)
async def getProfuctUpdateForm(request: Request, id: int):

    # note passing of parameters to the page
    return templates.TemplateResponse("product/partials/product_update_form.html", {"request": request, "product": getProduct(id) })

# https://fastapi.tiangolo.com/tutorial/request-form-models/#pydantic-models-for-forms
@router.put("/")
def putProduct(request: Request, productData: Annotated[Product, Form()]) :
    # get item value from the form POST data
    update_product = updateProduct(productData)
    return templates.TemplateResponse("product/partials/product_tr.html", {"request": request, "product": update_product})


@router.post("/")
def postProduct(
    request: Request,
    productData: Annotated[Product, Form()]
):
    # Call the service to add the new product
    new_product = newProduct(productData)
    
    # Render the new product row in the template
    return templates.TemplateResponse(
        "product/partials/product_tr.html", 
        {"request": request, "product": new_product}
    )

@router.delete("/{id}")
def delProduct(request: Request, id: int):
    deleteProduct(id)
    return templates.TemplateResponse("product/partials/product_list.html", {"request": request, "products": getAllProducts()})


@router.get("/filter/{category_id}", response_class=HTMLResponse)
async def filterProducts(request: Request, category_id: int):
    # Fetch products by category
    filtered_products = getProductsByCategory(category_id)
    return templates.TemplateResponse(
        "product/partials/product_list.html",
        {"request": request, "products": filtered_products}
    )
