import React, { useState } from "react";
import axios from "axios";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import './CreateEvent.css';

const CreateEvent = () => {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [startDate, setStartDate] = useState(new Date());
  const [endDate, setEndDate] = useState(null);
  const [events, setEvents] = useState([]);

  const createEvent = async () => {
    if (!title.trim()) {
      alert("Title is required!");
      return;
    }

    const eventData = {
      title: title,  // Correct key-value format
      description: description,
      start_time: startDate.toISOString(),
      end_time: endDate ? endDate.toISOString() : null,
    };

    try {
      const res = await axios.post("http://localhost:5000/add_events", eventData, {
        headers: {
          "Content-Type": "application/json" // ✅ Ensure JSON content type
        }
      });

      setEvents([...events, res.data.event]); // Append new event to list
      alert("Event created successfully!");
      resetForm();
    } catch (error) {
      console.error("Error creating event:", error);
      alert("Error creating event: " + (error.response?.data?.error || error.message));
    }
  };

  const resetForm = () => {
    setTitle("");
    setDescription("");
    setStartDate(new Date());
    setEndDate(null);
  };

  return (
    <div className="event-container">
      <h2>Create Event</h2>
      <input
        type="text"
        placeholder="Event Title"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
      />
      <textarea
        placeholder="Event Description"
        value={description}
        onChange={(e) => setDescription(e.target.value)}
      />
      <br />
      <label>Start Time:</label>
      <DatePicker selected={startDate} onChange={setStartDate} showTimeSelect />
      <br />
      <label>End Time:</label>
      <DatePicker selected={endDate} onChange={setEndDate} showTimeSelect isClearable />
      <br />
      <button onClick={createEvent}>Create Event</button>

      <h3>Created Events:</h3>
      <ul>
        {events.map((event, index) => (
          <li key={index}>
            <strong>{event.title}</strong> <br />
            {new Date(event.start_time).toLocaleString()} -{" "}
            {event.end_time ? new Date(event.end_time).toLocaleString() : "No End Time"}
            <br />
            {event.description}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default CreateEvent;
