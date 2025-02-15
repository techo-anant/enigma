from flask import request,app, jsonify
from .services import *
from . import *
from .model import StudyEvent, CalendarEvent
from icalendar import Calendar, Event
import datetime
from werkzeug.utils import secure_filename

#all the routes for notes like summarizing and extracting text from pdf
@app.route('/pdf_text', methods=['POST'])
def extract_text():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    # Save uploaded PDF temporarily
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    # Extract text from PDF
    extracted_text = extract_text_from_pdf(file_path)

    # Summarize extracted text
    summarized_text = summarize(extracted_text)

    # Delete file after processing
    os.remove(file_path)

    return jsonify({
        "summary": summarized_text
    })

#routes for Calendar events and ICS file generation
@app.route('/add_events', methods=['POST'])
def add_events():
    try:
        data = request.json
        if not data or 'event_name' not in data:
            return jsonify({'error': 'Event name is required'}), 400 # Bad request
        new_event = StudyEvent(
        title=data["title"],
        description=data.get("description", ""),
        start_time=datetime.datetime.fromisoformat(data["start_time"]),
        end_time=datetime.datetime.fromisoformat(data["end_time"]) if data.get("end_time") else None,
        link=data.get("link", ""),
    )

        db.session.add()
        db.session.commit()
        return jsonify({'message': f'Event added!", "event_id": {new_event.id}'}), 200 # OK

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route("/upload-ics", methods=["POST"])
def upload_ics():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    # Secure the filename and save the file
    file_path = os.path.join(UPLOAD_FOLDER, secure_filename(file.filename))
    file.save(file_path)

    # Parse the ICS file and store events
    extracted_events = parse_ics(file_path)
    return jsonify({"message": "Events extracted and stored!", "events": extracted_events})


def parse_ics(file_path):
    with open(file_path, "rb") as f:
        calendar = Calendar.from_ical(f.read())

    events_list = []
    with app.app_context():
        for component in calendar.walk():
            if component.name == "VEVENT":
                title = str(component.get("summary", "No Title"))
                description = str(component.get("description", "No Description"))
                start_time = str(component.get("dtstart").dt)
                end_time = str(component.get("dtend").dt) if component.get("dtend") else None
                location = str(component.get("location", "No Location"))

                # Store event in the database
                new_event = CalendarEvent(
                    title=title,
                    description=description,
                    start_time=start_time,
                    end_time=end_time,
                    location=location,
                )
                db.session.add(new_event)
                db.session.commit()

                # Append to list for response
                events_list.append({
                    "title": title,
                    "description": description,
                    "start_time": start_time,
                    "end_time": end_time,
                    "location": location,
                })

    return events_list




