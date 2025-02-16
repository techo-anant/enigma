from flask import request, jsonify, current_app
from werkzeug.utils import secure_filename
from datetime import *
from sqlalchemy import cast, Date, func
import os
from icalendar import Calendar, Event
from . import app, db
from .services import extract_text_from_pdf
from .model import StudyEvent, CalendarEvent


def parse_ics(file_path):
    events_list = []

    try:
        with open(file_path, "rb") as f:
            calendar = Calendar.from_ical(f.read())

        with app.app_context():  # Ensure database operations are inside app context
            for component in calendar.walk():
                if component.name == "VEVENT":
                    try:
                        start_time = component.get("dtstart").dt
                        end_time = component.get("dtend").dt if component.get("dtend") else None

                        if isinstance(start_time, datetime.date) and not isinstance(start_time, datetime.datetime):
                            start_time = datetime.datetime.combine(start_time, datetime.time.min)
                        if end_time and isinstance(end_time, datetime.date) and not isinstance(end_time, datetime.datetime):
                            end_time = datetime.datetime.combine(end_time, datetime.time.min)

                        new_event = CalendarEvent(
                            title=str(component.get("summary", "No Title")),
                            description=str(component.get("description", "No Description")),
                            start_time=start_time.isoformat(),
                            end_time=end_time.isoformat() if end_time else None,
                            location=str(component.get("location", "No Location")),
                        )

                        db.session.add(new_event)
                        events_list.append({
                            "title": new_event.title,
                            "start_time": start_time.isoformat(),
                            "end_time": end_time.isoformat() if end_time else None,
                            "location": new_event.location
                        })

                    except Exception as e:
                        current_app.logger.error(f"Error processing event: {str(e)}")
                        continue  # Skip to the next event

            db.session.commit()

    except Exception as e:
        with app.app_context():  # Ensure rollback is inside the app context
            db.session.rollback()
        current_app.logger.error(f"Database error: {str(e)}")
        raise

    return events_list

# Assuming necessary imports for db, models, and services are properly set up

# Routes for calendar events and ICS processing
@app.route('/add_events', methods=['POST'])
def add_events():
    try:
        data = request.json
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        # Validate required fields
        required_fields = ['title', 'start_time']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400

        # Create new event
        new_event = StudyEvent(
            title=data["title"],
            description=data.get("description", ""),
            start_time=datetime.datetime.fromisoformat(data["start_time"]),
            end_time=datetime.datetime.fromisoformat(data["end_time"]) if data.get("end_time") else None,
            link=data.get("link", ""),
        )

        db.session.add(new_event)  # Fixed missing argument
        db.session.commit()
        return jsonify({
            "message": "Event added!",
            "event_id": new_event.id  # Proper JSON structure
        }), 201  # Use 201 Created for new resources

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route("/upload-ics", methods=["POST", "GET"])
def upload_ics():
    if request.method == "GET":  # Fixed method check
        return jsonify({"message": "Upload an ICS file "
                                   "using POST"}), 200

    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    try:
        # File handling
        UPLOAD_FOLDER = current_app.config.get('UPLOAD_FOLDER', '/tmp')
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        filename = secure_filename(file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)

        # Process ICS
        events_list = parse_ics(file_path)
        return jsonify({
            "message": "Events extracted and stored!",
            "events": events_list
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)


@app.route("/events", methods=["GET"])
def get_events():
    date_str = request.args.get("date")  # Example: /events?date=2024-09-05

    if date_str:
        try:
            selected_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            print(f"\n🔎 Querying events for date: {selected_date}")

            # Fetch all events from database
            all_events = CalendarEvent.query.all()

            # ✅ Convert `start_time` to datetime object before filtering
            events = [
                event for event in all_events
                if str(event.start_time.date()) == selected_date
            ]

            print(f"\n✅ Found {len(events)} matching events.")

        except ValueError:
            return jsonify({"error": "Invalid date format. Use YYYY-MM-DD."}), 400
    else:
        events = CalendarEvent.query.all()

    # Convert events to JSON response
    events_data = [
        {
            "id": event.id,
            "title": event.title,
            "start_time": event.start_time,
            "end_time": event.end_time if event.end_time else None,
            "description": event.description if event.description else "No description",
            "location": event.location if event.location else "No location"
        }
        for event in events
    ]

    return jsonify(events_data), 200
