import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Navbar from "./navbar";
import UploadICS from "./UploadICS";
import CreateEvent from "./CreateEvent";
import BigCalendar from "./BigCalendar";
import Achievements from "./Achievements";
import ExamPrep from "./ExamPrep";
import Login from "./Login";

function App() {
  return (
    <Router>
      <Navbar />
      <Routes>
        <Route path="/" element={<h1>Home Page</h1>} />
        <Route path="/UploadICS" element={<UploadICS />} />
        <Route path="/navbar" element={<Navbar />} />
        <Route path="/CreateEvent" element={<CreateEvent />} />
        <Route path="/BigCalendar" element={<BigCalendar />} />
        <Route path="/ExamPrep" element={<ExamPrep />} />
        <Route path="/Login" element={<Login />} />
        <Route path="/Achievements" element={<Achievements />} />
      </Routes>
    </Router>
  );
}

export default App;
