import React, { useState, useEffect } from "react";
import { Calendar, momentLocalizer } from "react-big-calendar";
import moment from "moment";
import axios from "axios";
import "react-big-calendar/lib/css/react-big-calendar.css";

const localizer = momentLocalizer(moment);

const BigCalendar = () => {
    const [events, setEvents] = useState([]);
    const [selectedDate, setSelectedDate] = useState(null);
    const [filteredEvents, setFilteredEvents] = useState([]);

    // Fetch all events when the component loads
    useEffect(() => {
        axios.get("http://localhost:5000/events")
            .then((response) => {
                // Convert event date strings to Date objects
                const formattedEvents = response.data.map(event => ({
                    ...event,
                    start: new Date(event.start),
                    end: new Date(event.end),
                }));
                setEvents(formattedEvents);
            })
            .catch((error) => console.error("Error fetching events:", error));
    }, []);

    // Fetch events for a selected date
    const handleSelectSlot = async ({ start }) => {
        setSelectedDate(start);
        const formattedDate = moment(start).format("YYYY-MM-DD");

        try {
            const response = await axios.get(`http://localhost:5000/events?date=${formattedDate}`);

            // ✅ Ensure correct mapping from Flask API response
            const selectedEvents = response.data.map(event => ({
                id: event.id,
                title: event.title,
                start: moment(event.start_time).toDate(),  // Convert ISO 8601 string to Date
                end: event.end_time ? moment(event.end_time).toDate() : null,
                description: event.description,
                location: event.location
            }));

            setFilteredEvents(selectedEvents);
        } catch (error) {
            console.error("Error fetching events for date:", error);
            setFilteredEvents([]); // Reset if error
        }
    };

    return (
        <div style={{ height: "600px", padding: "20px", color: "black" }}>
            <h2>📅 Event Calendar</h2>
            <Calendar
                localizer={localizer}
                events={events}
                startAccessor="start"
                endAccessor="end"
                selectable
                onSelectSlot={handleSelectSlot} // Click to fetch events for that date
                style={{ height: "500px" }}
                views={["month", "week", "day", "agenda"]}
            />

            {/* Show Event Details Modal when date is clicked */}
            {selectedDate && (
                <div className="event-details">
                    <h3>Events on {moment(selectedDate).format("MMMM Do, YYYY")}</h3>
                    {filteredEvents.length > 0 ? (
                        <ul>
                            {filteredEvents.map((event, index) => (
                                <li key={index}>
                                    <strong>{event.title}</strong> <br />
                                    {moment(event.start).format("h:mm A")} - {moment(event.end).format("h:mm A")}
                                    <p>{event.description}</p>
                                </li>
                            ))}
                        </ul>
                    ) : (
                        <p>No events on this date.</p>
                    )}
                    <button onClick={() => setSelectedDate(null)}>Close</button>
                </div>
            )}
        </div>
    );
};

export default BigCalendar;
