import React, { useState } from "react";
import axios from "axios";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";

const CreateEvent = () => {
  const [summary, setSummary] = useState("");
  const [startDate, setStartDate] = useState(new Date());
  const [endDate, setEndDate] = useState(new Date());
  const [events, setEvents] = useState([]);

  const createEvent = async () => {
    const event = {
      summary,
      start: startDate.toISOString(),
      end: endDate.toISOString(),
    };

    try {
      const res = await axios.post("http://localhost:5000/create-event", event);
      setEvents(res.data.events);
      alert("Event created and saved as ICS!");
    } catch (error) {
      alert("Error creating event: " + error.response.data.error);
    }
  };

  return (
    <div>
      <h2>Create Event</h2>
      <input
        type="text"
        placeholder="Event Summary"
        value={summary}
        onChange={(e) => setSummary(e.target.value)}
      />
      <br />
      <label>Start Time:</label>
      <DatePicker selected={startDate} onChange={(date) => setStartDate(date)} showTimeSelect />
      <br />
      <label>End Time:</label>
      <DatePicker selected={endDate} onChange={(date) => setEndDate(date)} showTimeSelect />
      <br />
      <button onClick={createEvent}>Create Event</button>

      <h3>Created Events:</h3>
      <ul>
        {events.map((event, index) => (
          <li key={index}>
            {event.summary} - {new Date(event.start).toLocaleString()} to {new Date(event.end).toLocaleString()}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default CreateEvent;
