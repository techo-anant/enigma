import React, { useState } from "react";
import axios from "axios";

const UploadICS = () => {
  const [file, setFile] = useState(null);
  const [events, setEvents] = useState([]);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const uploadICS = async () => {
    if (!file) return alert("Please select an .ics file");

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await axios.post("http://localhost:5000/upload-ics", formData);
      setEvents(res.data.events);
      alert("ICS file uploaded and parsed successfully!");
    } catch (error) {
      alert("Error uploading file: " + error.response.data.error);
    }
  };

  return (
    <div>
      <h2>Upload ICS File</h2>
      <input type="file" accept=".ics" onChange={handleFileChange} />
      <button onClick={uploadICS}>Upload</button>

      <h3>Events from ICS:</h3>
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

export default UploadICS;
