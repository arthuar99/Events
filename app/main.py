from fastapi import FastAPI
from app.database.session import Base, engine
from app.models import User, Event, Booking
from app.routers import auth, events, bookings, tickets, frontend
# from app.routers import bookings

# Create database tables
Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(
    title="Event Booking API",
    description="A comprehensive API for event booking and management",
    version="1.0.0"
)

# Include routers (each router defines its own prefix)
app.include_router(auth.router, tags=["Authentication"])  
app.include_router(events.router, tags=["Events"])        
app.include_router(bookings.router, tags=["Bookings"])    
app.include_router(bookings.bookings_router, tags=["Bookings"])  # Add user bookings router
app.include_router(tickets.router, tags=["Tickets"])      
app.include_router(frontend.router, tags=["Frontend"])    

# Remove duplicate home route - frontend router handles it
# @app.get("/")
# def health():
#     return {"status": "ok", "message": "Event Booking API is running"}