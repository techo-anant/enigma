import React, { useState } from "react";
import axios from "axios";
import { useDropzone } from "react-dropzone";
import './ExamPrep.css'; // ChatGPT-style UI

const ExamPrep = () => {
    const [selectedFile, setSelectedFile] = useState(null);
    const [chatMessages, setChatMessages] = useState([]);
    const [flashcard, setFlashcard] = useState("");

    // Handle file selection
    const { getRootProps, getInputProps } = useDropzone({
        accept: ".txt, .pdf",
        onDrop: (acceptedFiles) => {
            setSelectedFile(acceptedFiles[0]);
            addChatMessage("User", `📂 Selected file: ${acceptedFiles[0].name}`);
        },
    });

    // Function to add chat messages
    const addChatMessage = (sender, message) => {
        setChatMessages((prev) => [...prev, { sender, message }]);
    };

    // Upload file and get summary
    const uploadFile = async () => {
        if (!selectedFile) {
            addChatMessage("System", "⚠️ Please select a file first!");
            return;
        }

        const formData = new FormData();
        formData.append("file", selectedFile);

        addChatMessage("User", "📤 Uploading file...");

        try {
            const response = await axios.post("http://localhost:5000/upload-file", formData, {
                headers: { "Content-Type": "multipart/form-data" },
            });

            addChatMessage("AI", `📖 Summary: ${response.data.summary}`);
        } catch (error) {
            addChatMessage("System", "❌ Error uploading file. Try again.");
        }
    };

    // Convert summary into flashcards
    const generateFlashcard = () => {
        if (!flashcard.trim()) {
            addChatMessage("System", "⚠️ Enter text to create a flashcard!");
            return;
        }

        addChatMessage("User", `📝 Created flashcard: "${flashcard}"`);
        setFlashcard("");
    };

    return (
        <div className="chat-container">
            <div className="chat-box">
                {chatMessages.map((msg, index) => (
                    <div key={index} className={`chat-message ${msg.sender}`}>
                        <span>{msg.message}</span>
                    </div>
                ))}
            </div>

            <div {...getRootProps()} className="dropzone">
                <input {...getInputProps()} />
                {selectedFile ? (
                    <p>📂 {selectedFile.name}</p>
                ) : (
                    <p>Drag & drop a TXT or PDF file here, or click to select one</p>
                )}
            </div>

            <button onClick={uploadFile} id="summary">Upload & Summarize</button>

            <div className="flashcard-input">
                <input
                    type="text"
                    placeholder="Enter text for flashcard..."
                    value={flashcard}
                    onChange={(e) => setFlashcard(e.target.value)}
                    className="flash-text"
                />
                <button onClick={generateFlashcard} id="flash-button">Create Flashcard</button>
            </div>
        </div>
    );
};

export default ExamPrep;