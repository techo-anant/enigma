import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Navbar from "./navbar";
import UploadICS from "./UploadICS";
import CreateEvent from "./CreateEvent";

function App() {
  return (
    <Router>
      <Navbar />
      <Routes>
        <Route path="/" element={<h1>Home Page</h1>} />
        <Route path="/UploadICS" element={<UploadICS />} />
        <Route path="/navbar" element={<Navbar />} />
        <Route path="/CreateEvent" element={<CreateEvent />} />
      </Routes>
    </Router>
  );
}

export default App;
