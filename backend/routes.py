from flask import request,app, jsonify
from .services import *
from . import *
from .model import StudyEvent
from ics import Calendar, Event
import datetime

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

@app.route('/generate-ics/<int:event_id>', methods=['GET'])
def generate_ics(event_id):
    event = StudyEvent.query.get(event_id)
    if not event:
        return jsonify({"error": "Event not found"}), 404

    calendar = Calendar()
    cal_event = Event()
    cal_event.name = event.title
    cal_event.begin = event.start_time
    cal_event.description = event.description
    if event.end_time:
        cal_event.end = event.end_time
    if event.link:
        cal_event.url = event.link

    calendar.events.add(cal_event)

    ics_file_path = f"uploads/event_{event_id}.ics"
    with open(ics_file_path, "w") as file:
        file.writelines(calendar)

    return jsonify({"message": "ICS file generated!", "ics_file": ics_file_path})