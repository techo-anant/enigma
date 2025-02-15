import { GoogleOAuthProvider, GoogleLogin } from "@react-oauth/google";

const clientId = "YOUR_GOOGLE_CLIENT_ID";

function GoogleAuth() {
    return (
        <GoogleOAuthProvider clientId={clientId}>
            <GoogleLogin
                onSuccess={(response) => {
                    console.log("Google Login Success:", response);
                    fetchUserCalendar(response.credential);
                }}
                onError={() => console.log("Login Failed")}
            />
        </GoogleOAuthProvider>
    );
}

function fetchUserCalendar(token) {
    fetch("http://localhost:5000/get-calendar-events", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ token }),
    })
    .then((res) => res.json())
    .then((data) => console.log("Calendar Events:", data))
    .catch((err) => console.error(err));
}

export default GoogleAuth;
