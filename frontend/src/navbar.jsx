import './navbar.css'

const navbar = () => {
    return (
        <nav class="navbar">
            <div class="logo">StudyTool</div>
            <ul class="nav-links">
                <li><a href="#">Home</a></li>
                <li><a href="#">Study Map</a></li>
                <li><a href="#">Calendar</a></li>
                <li><a href="#">Notes</a></li>
                <li><a href="#">Exam Prep</a></li>
                <li><a href="#">Achievements</a></li>
            </ul>
        </nav>
    );
}

export default navbar;