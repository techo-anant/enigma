from flask import request, jsonify, current_app, render_template
from werkzeug.utils import secure_filename
import os
from .model import StudyEvent, CalendarEvent
import datetime
from datetime import datetime
from icalendar import Calendar
from backend import db, app
from backend.model import CalendarEvent, StudyEvent, User
from flask import current_app
from flask_login import login_user, logout_user
from flask_login import login_required, current_user

@app.route("/login", methods=["POST"])
def login():
    try:
        data = request.json
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        # Extract user details
        user_email = data.get("email")
        user_name = data.get("name")
        user_image = data.get("image", "default.jpg")  # Default profile image

        if not user_email or not user_name:
            return jsonify({'error': 'Missing required fields'}), 400

        # Check if the user already exists
        user = User.query.filter_by(email=user_email).first()

        if not user:
            # Create new user
            user = User(
                name=user_name,
                email=user_email,
                image_file=user_image,
                Level=1,  # Default level
                experience=0  # Default experience
            )
            db.session.add(user)
            db.session.commit()

        # Log the user in
        login_user(user, remember=True)


        return jsonify({
            "message": "Login successful",
            "user": {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "image": user.image_file,
                "level": user.Level,
                "experience": user.experience
            }
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


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
            all_events = CalendarEvent.query.all() + StudyEvent.query.all()
 
 
            # ✅ Convert `start_time` to datetime object before filtering
            events = [
                event for event in all_events 
                if event.start_time.date() == selected_date
            ]
 
            print(f"\n✅ Found {len(events)} matching events.")
 
        except ValueError:
            return jsonify({"error": "Invalid date format. Use YYYY-MM-DD."}), 400
    else:
        events = CalendarEvent.query.all() + StudyEvent.query.all()
 
    # Convert events to JSON response
    events_data = [
        {
            "id": event.id,
            "title": event.title,
            "start_time": event.start_time,
            "end_time": event.end_time if event.end_time else None,
            "description": event.description if event.description else "No description"
        }
        for event in events
    ]
 
    return jsonify(events_data), 200

@app.route("/list_events", methods=["GET"])
def events():
    events = CalendarEvent.query.all()
    return render_template("index.html", events=events, title = "events")

@app.route('/add_events', methods=['POST'])
def add_events():
    # ✅ Ensure request is a POST request
    if request.method != "POST":
        return jsonify({"error": "Use POST method to create events"}), 405
 
    # ✅ Ensure the request is JSON
    if not request.is_json:
        return jsonify({'error': 'Request must be JSON'}), 400
 
    try:
        data = request.get_json()  # ✅ Use `get_json()` to safely parse JSON
 
        # Validate required fields
        required_fields = ['title', 'start_time']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
 
        # Convert start_time and end_time from ISO format
        start_time = datetime.fromisoformat(data["start_time"])
        end_time = datetime.fromisoformat(data["end_time"]) if data.get("end_time") else None
 
        # Create new event
        new_event = StudyEvent(
            title=data["title"],
            description=data.get("description", ""),
            start_time=start_time,
            end_time=end_time,
            link=data.get("link", ""),
        )
 
        db.session.add(new_event)
        db.session.commit()
 
        return jsonify({
            "message": "Event added successfully!",
            "event_id": new_event.id,
            "event": {
                "title": new_event.title,
                "description": new_event.description,
                "start_time": new_event.start_time.isoformat(),
                "end_time": new_event.end_time.isoformat() if new_event.end_time else None,
                "link": new_event.link
            }
        }), 201  # HTTP 201 Created
 
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500