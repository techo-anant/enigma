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
from services import extract_text_from_pdf, summarize

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
        login_user(user)

        # Fetch user's StudyEvents and CalendarEvents
        study_events = StudyEvent.query.filter_by(user_id=user.id).all()
        calendar_events = CalendarEvent.query.filter_by(user_id=user.id).all()

        # Format events for JSON response
        study_events_data = [
            {
                "id": event.id,
                "title": event.title,
                "description": event.description,
                "start_time": event.start_time.isoformat(),
                "end_time": event.end_time.isoformat() if event.end_time else None,
                "link": event.link
            }
            for event in study_events
        ]

        calendar_events_data = [
            {
                "id": event.id,
                "title": event.title,
                "description": event.description,
                "start_time": event.start_time.isoformat(),
                "end_time": event.end_time.isoformat() if event.end_time else None,
                "location": event.location
            }
            for event in calendar_events
        ]

        return jsonify({
            "message": "Login successful",
            "user": {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "image": user.image_file,
                "level": user.Level,
                "experience": user.experience
            },
            "study_events": study_events_data,
            "calendar_events": calendar_events_data
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

def parse_ics(file_path):
    events_list = []
    try:
        with open(file_path, "rb") as f:
            calendar = Calendar.from_ical(f.read())

        if not current_user.is_authenticated:
            return {"error": "User not authenticated"}, 401  # Ensure user is logged in

        with app.app_context():  # Ensure database operations are inside app context
            for component in calendar.walk():
                if component.name == "VEVENT":
                    try:
                        start_time = component.get("dtstart").dt
                        end_time = component.get("dtend").dt if component.get("dtend") else None

                        # Ensure correct datetime formatting
                        if isinstance(start_time, datetime.date) and not isinstance(start_time, datetime.datetime):
                            start_time = datetime.combine(start_time, datetime.min.time())
                        if end_time and isinstance(end_time, datetime.date) and not isinstance(end_time, datetime.datetime):
                            end_time = datetime.combine(end_time, datetime.min.time())

                        # Check if the event already exists for the user
                        existing_event = CalendarEvent.query.filter_by(
                            title=str(component.get("summary", "No Title")),
                            start_time=start_time,
                            user_id=current_user.id  # Check if the user already has this event
                        ).first()

                        if existing_event:
                            # Update existing event
                            existing_event.description = str(component.get("description", "No Description"))
                            existing_event.end_time = end_time
                            existing_event.location = str(component.get("location", "No Location"))
                        else:
                            # Create new event
                            new_event = CalendarEvent(
                                title=str(component.get("summary", "No Title")),
                                description=str(component.get("description", "No Description")),
                                start_time=start_time,
                                end_time=end_time,
                                location=str(component.get("location", "No Location")),
                                user_id=current_user.id  # Associate event with user
                            )
                            db.session.add(new_event)

                        events_list.append({
                            "title": str(component.get("summary", "No Title")),
                            "start_time": start_time.isoformat(),
                            "end_time": end_time.isoformat() if end_time else None,
                            "location": str(component.get("location", "No Location"))
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
            all_events = CalendarEvent.query.all()

            # ✅ Convert `start_time` to datetime object before filtering
            events = [
                event for event in all_events
                if event.start_time.date() == selected_date
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

@app.route("/list_events", methods=["GET"])
def events():
    events = CalendarEvent.query.all()
    return render_template("index.html", events=events, title = "events")

@app.route('/add_events', methods=['POST'])
@login_required  # Ensures only logged-in users can add events
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

        # Ensure the user is logged in
        if not current_user.is_authenticated:
            return jsonify({'error': 'User not authenticated'}), 401

        # Create new event linked to the current user
        new_event = StudyEvent(
            title=data["title"],
            description=data.get("description", ""),
            start_time=datetime.fromisoformat(data["start_time"]),
            end_time=datetime.fromisoformat(data["end_time"]) if data.get("end_time") else None,
            link=data.get("link", ""),
            user_id=current_user.id  # Associate the event with the logged-in user
        )

        # Add to the database
        db.session.add(new_event)
        db.session.commit()

        return jsonify({
            "message": "Event added!",
            "event_id": new_event.id,
            "user_id": current_user.id  # Confirming event is linked to user
        }), 201  # 201 Created status

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route("/upload-pdf", methods=["POST"])
def upload_pdf():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    try:
        # Save the uploaded file
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(file_path)

        # Extract text from PDF
        extracted_text = extract_text_from_pdf(file_path)

        if not extracted_text:
            return jsonify({"error": "Failed to extract text from the PDF"}), 500

        # Summarize extracted text
        summary_response = summarize(extracted_text)

        return jsonify({
            "message": "Summarization completed",
            "summary": summary_response.get("generated_text", "Summarization failed"),
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        # Cleanup: Remove the uploaded file after processing
        if os.path.exists(file_path):
            os.remove(file_path)