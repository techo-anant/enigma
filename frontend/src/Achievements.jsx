import React from 'react';
import './Achievements.css';
import bgImage from './assets/bg-image.jpg'; // Import image
import photo from './assets/anant-photo.jpeg'

const Achievements = () => {

    const user_data = [{
        "id": 1,
        "Name": "Anant Kumar Singh",
        "Email": "singh4n3@uwindsor.ca",
        "Level": 1,
        "Experience": 9 // Experience value
    }];

    return (
        <div>
            <div className="achievements">
                <img src={bgImage} alt="Background Image" className="image" />
                <div className='rowitem'><img src={photo} alt="your-image" className="photo" />
                    <div className="data">
                        {user_data.map((user) => (
                            <div className="user_data" key={user.id}>
                                <p id="name">{user.Name}</p>
                                <p id="email"><b>Login ID:</b> {user.Email}</p>
                                <span id="level">Level: {user.Level}</span>

                                {/* Experience Bar Section */}
                                <div id="experience">
                                    <div className="progress-bar">
                                        <div
                                            className="progress-fill"
                                            style={{ width: `${user.Experience}%` }}  // <-- Dynamically set width
                                        ></div>
                                    </div>
                                    <span className="exp-text">Exp: {user.Experience} / 100</span>
                                </div>

                            </div>
                        ))}
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Achievements;
