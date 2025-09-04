from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.core.deps import get_current_user_optional

router = APIRouter(tags=["Frontend"])

# Setup Jinja2 templates
templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Home page"""
    try:
        user = await get_current_user_optional(request)
        return templates.TemplateResponse("index.html", {"request": request, "current_user": user})
    except Exception as e:
        # Fallback if user fetch fails
        return templates.TemplateResponse("index.html", {"request": request, "current_user": None})

@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    """Login page"""
    try:
        return templates.TemplateResponse("login.html", {"request": request})
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to load login page")

@router.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    """Register page"""
    try:
        return templates.TemplateResponse("register.html", {"request": request})
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to load register page")

@router.get("/events", response_class=HTMLResponse)
async def events_page(request: Request):
    """Events page"""
    try:
        user = await get_current_user_optional(request)
        return templates.TemplateResponse("events.html", {"request": request, "current_user": user})
    except Exception as e:
        return templates.TemplateResponse("events.html", {"request": request, "current_user": None})

@router.get("/bookings", response_class=HTMLResponse)
async def bookings_page(request: Request):
    """Bookings page"""
    try:
        user = await get_current_user_optional(request)
        return templates.TemplateResponse("bookings.html", {"request": request, "current_user": user})
    except Exception as e:
        return templates.TemplateResponse("bookings.html", {"request": request, "current_user": None})

@router.get("/scanner", response_class=HTMLResponse)
async def scanner_page(request: Request):
    """QR Scanner page for organizers"""
    try:
        user = await get_current_user_optional(request)
        return templates.TemplateResponse("scanner.html", {"request": request, "current_user": user})
    except Exception as e:
        return templates.TemplateResponse("scanner.html", {"request": request, "current_user": None})
