def ticket_email_html(event_title: str, seat_number: int, verify_url: str) -> str:
    return f"""
    <h2>Your Ticket</h2>
    <p>Event: <b>{event_title}</b></p>
    <p>Seat: <b>{seat_number}</b></p>
    <p>Verify at: <a href="{verify_url}">{verify_url}</a></p>
    """
