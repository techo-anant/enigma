import React, { useState } from "react";
import axios from "axios";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import "./CreateEvent.css";

const CreateEvent = () => {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [startDate, setStartDate] = useState(new Date());
  const [endDate, setEndDate] = useState(new Date());
  const [events, setEvents] = useState([]);

  const createEvent = async () => {
    if (!title.trim()) {
      alert("Event title is required!");
      return;
    }

    const eventData = {
      title,
      description,
      start_time: startDate.toISOString(),
      end_time: endDate.toISOString(),
    };

    try {
      const res = await axios.post("http://localhost:5000/add_events", eventData, {
        headers: { "Content-Type": "application/json" },
      });

      setEvents([...events, res.data.event]); // Append new event to list
      alert("Event created successfully!");

      // Reset form fields
      resetForm();
    } catch (error) {
      console.error("Error creating event:", error);
      alert("Error creating event: " + (error.response?.data?.error || "Unknown error"));
    }
  };

  const resetForm = () => {
    setTitle("");
    setDescription("");
    setStartDate(new Date());
    setEndDate(new Date());
  };

  return (
    <div className="create-event-container">
      <div className="create-event">
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
        <div className="datepicker-container">
          <DatePicker
            selected={startDate}
            onChange={(date) => setStartDate(date)}
            showTimeSelect
            dateFormat="Pp"
          />
        </div>

        <label>End Time:</label>
        <div className="datepicker-container">
          <DatePicker
            selected={endDate}
            onChange={(date) => setEndDate(date)}
            showTimeSelect
            dateFormat="Pp"
          />
        </div>

        <br />
        <button onClick={createEvent}>Create Event</button>

        <h3>Created Events:</h3>
        <ul className="list-events">
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
    </div>
  );
};

export default CreateEvent;
