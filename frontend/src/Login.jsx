import "./Login.css";
import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

const Login = () => {
    const navigate = useNavigate();
    const [name, setName] = useState("");
    const [email, setEmail] = useState("");

    // ✅ Check if user is already logged in
    useEffect(() => {
        const storedUser = JSON.parse(localStorage.getItem("user"));
        if (storedUser) {
            console.log("User already logged in:", storedUser);
            navigate("/Achievements", { state: { user: storedUser } });
        }
    }, [navigate]);

    // Handle form submission
    const handleSubmit = async () => {
        if (!name.trim() || !email.trim()) {
            alert("Please enter both name and email!");
            return;
        }

        try {
            const response = await axios.post("http://localhost:5000/login", {
                name: name,
                email: email,
            });

            if (response.status === 200) {
                console.log("User logged in successfully.");

                // ✅ Store user data in localStorage
                localStorage.setItem("user", JSON.stringify(response.data.user));

                // ✅ Navigate to Achievements with user data
                navigate("/Achievements", { state: { user: response.data.user } });
            } else {
                alert(response.data.error || "Login failed. Try again.");
            }
        } catch (error) {
            alert("Error logging in: " + (error.response?.data?.error || error.message));
        }
    };

    return (
        <div className="login">
            <h1>Login</h1>
            <div className="label">
                <p>Name</p>
            </div>
            <input
                type="text"
                name="Name"
                id="Name"
                placeholder="Your Name"
                value={name}
                onChange={(e) => setName(e.target.value)}
            />
            <div className="label">
                <p>Email</p>
            </div>
            <input
                type="email"
                name="email"
                id="email"
                placeholder="Your Email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
            />
            <button id="submit" onClick={handleSubmit}>See Your Achievements</button>
        </div>
    );
};

export default Login;
