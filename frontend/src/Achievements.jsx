import React, { useReducer } from 'react';
import './Achievements.css';
import bgImage from './assets/bg-image.jpg'; // Import image
import photo from './assets/anant-photo.jpeg'


const Achievements = () => {

    const user_data = [{
        "id": 1,
        "Name": "Anant Kumar Singh",
        "Email": "singh4n3@uwindsor.ca",
        "Level": 1,
        "Experience": 9
    }];


    return (
        <div>
            <div className="achievements">
                <img src={bgImage} alt="Background Image" className="image" />
                <img src={photo} alt="your-image" className="photo" />
                <div className="data">
                    {user_data.map((user_data) => (
                        <div className="user_data" key={user_data.id}>
                            <p id="name">{user_data.Name}</p>
                            <p id="email">{user_data.Email}</p>
                            <span id="level">Level: {user_data.Level}</span>
                            <div id="experience">Exp: {user_data.Experience}</div>
                        </div>
                    ))}
                </div>
            </div>


        </div>
    );
};

export default Achievements;
