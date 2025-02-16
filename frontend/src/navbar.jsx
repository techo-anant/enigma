import './navbar.css'

const navbar = () => {
    return (
        <nav class="navbar">
            <div class="logo">StudyTool</div>
            <ul class="nav-links">
                <li><a href="#">Home</a></li>
                <li><a href="http://localhost:5173/UploadICS">Upload ics</a></li>
                <li><a href="http://localhost:5173/BigCalendar">Calendar</a></li>
                <li><a href="http://localhost:5173/CreateEvent">Create Event</a></li>
                <li><a href="#">Exam Prep</a></li>
                <li><a href="http://localhost:5173/Achievements">Achievements</a></li>
            </ul>
        </nav>
    );
}

export default navbar;