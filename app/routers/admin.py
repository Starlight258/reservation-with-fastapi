from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.config import TEMPLATES_DIR

router = APIRouter()
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))


@router.get("/admin", response_class=HTMLResponse)
async def show_admin_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="admin/index.html",
        context={"request": request}
    ) 