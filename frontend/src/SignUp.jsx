import './SignUp.css';
import { useState } from 'react';
import { useNavigate } from "react-router-dom";

const SignUp = () => {

    const navigate = useNavigate();

    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [confirmPassword, setConfirmPassword] = useState("");
    const [errorMessage, setErrorMessage] = useState("");

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await fetch('http://localhost:5000/sign_up', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ username, password }),
            });

            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }

            const data = await response.json(); // Correct response type
            console.log(data);  // Log server response
            alert(data.message);  // Show success message
        } catch (error) {
            console.error('Fetch error:', error); // Debugging log
            alert('An error occurred. Please try again.');
        }
    };


    // const handleSubmit = (e) => {
    //     e.preventDefault();
    //     if(password.length < 8){
    //         setErrorMessage("Password must be at least 8 characters long");
    //     }else if(password !== confirmPassword){
    //         setErrorMessage("Passwords do not match");
    //     }else{
    //         setErrorMessage("");
    //         const username = document.getElementById("username").value;
    //         const users = JSON.parse(localStorage.getItem("users")) || [];
    //         const userExists = users.some(
    //             (user) => user.username === username
    //         );
    //         if(userExists){
    //             setTimeout(setErrorMessage("Username already exists, please login."), 3000);
    //         }else{
    //             let users = JSON.parse(localStorage.getItem("users")) || [];
    //             users.push({ username, password });
    //             localStorage.setItem("users", JSON.stringify(users));
    //             console.log("Passwords matched & Form submitted");
    //         }
    //         navigate("/");
    //     }
    // };


    return (
        <div className="sign-up">
            <h1>Sign Up</h1>
            <form onSubmit={handleSubmit}>
                <label htmlFor="username">Username</label><br />
                <input type="email" name="username" id="username"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    required /><br />
                <label htmlFor="password">Password</label><br />
                <input type="password"
                    name="password"
                    id="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required minLength={8} /><br />
                <label htmlFor="confirm-password">Confirm Password</label><br />
                <input type="password"
                    name="confirm-password"
                    id="confirm-password"
                    value={confirmPassword}
                    onChange={(e) => setConfirmPassword(e.target.value)}
                    required minLength={8} /><br />

                <div className="error">{errorMessage}</div>
                <input type="submit" value="Sign Up" id='submit' />
            </form>
        </div>
    );
}

export default SignUp;