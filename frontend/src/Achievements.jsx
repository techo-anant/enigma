import React, { useEffect, useState } from 'react';
import { useLocation, useNavigate } from "react-router-dom";
import axios from "axios";
import './Achievements.css';
import bgImage from './assets/bg-image.jpg'; // Import image
import photo from './assets/anant-photo.jpeg';

const Achievements = () => {
    const location = useLocation();
    const navigate = useNavigate();
    const [user, setUser] = useState(null);

    // ✅ Load user data from localStorage or backend
    useEffect(() => {
        const storedUser = JSON.parse(localStorage.getItem("user"));

        if (storedUser) {
            setUser(storedUser);
            fetchUserData(storedUser.email);  // ✅ Fetch latest user data
        } else if (location.state?.user) {
            setUser(location.state.user);
            localStorage.setItem("user", JSON.stringify(location.state.user));  // Save if passed via navigation
        } else {
            navigate("/Login"); // ✅ First redirect to Login
            setTimeout(() => {
                alert("Please Login First."); // ✅ Show alert after navigation
            }, 500);
        }
    }, [navigate, location.state]);

    // ✅ Fetch user data from backend to keep it updated
    const fetchUserData = async (email) => {
        try {
            const response = await axios.get(`http://localhost:5000/user/${email}`);
            if (response.status === 200) {
                setUser(response.data.user);
                localStorage.setItem("user", JSON.stringify(response.data.user));  // ✅ Update localStorage
            }
        } catch (error) {
            console.error("Error fetching user data:", error);
        }
    };

    // ✅ Logout Function
    const handleLogout = () => {
        localStorage.removeItem("user");  // ✅ Remove user from localStorage
        navigate("/Login");  // ✅ Redirect to login page
    };

    if (!user) {
        return <p>Loading...</p>;
    }

    return (
        <div>
            <div className="achievements">
                <img src={bgImage} alt="Background Image" className="image" />
                <div className='rowitem'>
                    <img src={photo} alt="User" className="photo" />
                    <div className="data">
                        <div className="user_data">
                            <p id="name">{user.name}</p>
                            <p id="email"><b>Login ID:</b> {user.email}</p>
                            <span id="level">Level: {user.level}</span>

                            {/* Experience Bar Section */}
                            <div id="experience">
                                <div className="progress-bar">
                                    <div
                                        className="progress-fill"
                                        style={{ width: `${user.experience}%` }}
                                    ></div>
                                </div>
                                <span className="exp-text">Exp: {user.experience} / 100</span>
                            </div>

                            {/* ✅ Logout Button */}
                            <button className="logout-btn" onClick={handleLogout}>
                                Logout
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Achievements;
