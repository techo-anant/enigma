import React, { useState, useEffect } from "react";
import { Calendar, momentLocalizer } from "react-big-calendar";
import moment from "moment";
import axios from "axios";
import "react-big-calendar/lib/css/react-big-calendar.css";
import './BigCalendar.css';

const localizer = momentLocalizer(moment);

const BigCalendar = () => {
    const [events, setEvents] = useState([]);
    const [selectedDate, setSelectedDate] = useState(null);
    const [filteredEvents, setFilteredEvents] = useState([]);
    const [date, setDate] = useState(new Date()); // Track current calendar date
    const [view, setView] = useState("month"); // Track current view (month/week/day)

    // Fetch all events when the component loads
    useEffect(() => {
        axios.get("http://localhost:5000/events")
            .then((response) => {
                const formattedEvents = response.data.map(event => ({
                    ...event,
                    start: new Date(event.start),
                    end: new Date(event.end),
                }));
                setEvents(formattedEvents);
            })
            .catch((error) => console.error("Error fetching events:", error));
    }, []);

    const handleSelectSlot = async ({ start }) => {
        setSelectedDate(start);
        const formattedDate = moment(start).format("YYYY-MM-DD");

        try {
            const response = await axios.get(`http://localhost:5000/events?date=${formattedDate}`);
            const selectedEvents = response.data.map(event => ({
                id: event.id,
                title: event.title,
                start: moment(event.start_time).toDate(),
                end: event.end_time ? moment(event.end_time).toDate() : null,
                description: event.description,
                location: event.location
            }));
            setFilteredEvents(selectedEvents);
        } catch (error) {
            console.error("Error fetching events for date:", error);
            setFilteredEvents([]);
        }
    };

    return (
        <div className="calendar-container">
            <span id="cal-name">Event Calendar</span>
            <Calendar
                localizer={localizer}
                events={events}
                startAccessor="start"
                endAccessor="end"
                selectable
                onSelectSlot={handleSelectSlot}
                style={{ height: "500px" }}
                views={["month", "week", "day", "agenda"]}
                date={date} // Controlled current date
                view={view} // Controlled current view
                onNavigate={setDate} // Update date on navigation
                onView={setView} // Update view when changing views
            />

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