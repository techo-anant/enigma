import React, { useState } from "react";
import { Calendar, momentLocalizer } from "react-big-calendar";
import moment from "moment";
import "react-big-calendar/lib/css/react-big-calendar.css";

const localizer = momentLocalizer(moment);

const BigCalendar = () => {
    const [events, setEvents] = useState([
        { title: "Meeting", start: new Date(), end: new Date() },
    ]);

    return (
        <div style={{ height: "500px" }}>
            <h2>Big Calendar</h2>
            <Calendar
                localizer={localizer}
                events={events}
                startAccessor="start"
                endAccessor="end"
                style={{ height: 400 }}
            />
        </div>
    );
};

export default BigCalendar;
