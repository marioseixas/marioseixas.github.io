---
layout: default
title: Events
permalink: /events
icon: "far fa-calendar"
---

<center>
<h2 class="title"> <i class="far fa-calendar"></i> Events </h2>
</center>

<html lang='de'>
  <head>
    <meta charset='utf-8' />
    <script src='/assets/js/vendor/fullcalendar/index.global.min.js'></script>
    <script src='/assets/js/vendor/fullcalendar/de.global.min.js'></script>
    <script src='https://cdnjs.cloudflare.com/ajax/libs/ical.js/1.5.0/ical.min.js'></script>
    <script>
      document.addEventListener('DOMContentLoaded', function() {
        var calendarEl = document.getElementById('calendar');
        var calendar = new FullCalendar.Calendar(calendarEl, {
          initialView: 'dayGridMonth',
          height: "auto",
          locale: 'de',
          events: function(fetchInfo, successCallback, failureCallback) {
            fetch('https://calendar.google.com/calendar/ical/marioseixascardosoneto%40gmail.com/public/basic.ics')
              .then(response => response.text())
              .then(data => {
                const jcalData = ICAL.parse(data);
                const comp = new ICAL.Component(jcalData);
                const events = comp.getAllSubcomponents('vevent').map(vevent => {
                  const event = new ICAL.Event(vevent);
                  return {
                    title: event.summary,
                    start: event.startDate.toJSDate(),
                    end: event.endDate.toJSDate(),
                    description: event.description,
                    location: event.location
                  };
                });
                successCallback(events);
              })
              .catch(error => failureCallback(error));
          },
          weekNumbers: true,
          headerToolbar: {
            left: 'today',
            center: 'title',
            right: 'prev,next'
          }
        });
        calendar.render();
      });
    </script>
  </head>
  <body>
    <div id='calendar' style="width:95%; margin: auto;"></div>
    <div style="display: flex; flex-direction: column; justify-content: center; align-items: center; border: 1px">
      <div style="display: flex; align-items: center; margin-top: 50px">
        <p>iCal-Feed:
          <code id="icalFeedUrl" style="box-shadow: 0px 0px 10px 0px rgba(0, 0, 0, 0.1); font-family: monospace;"></code>
        </p>
        <a id="copyButton" class="button" style="margin-left: 10px; margin-top: 0px">
          <i class="fas fa-copy" title="In Zwischenablage kopieren"></i>
        </a>
      </div>
    </div>

    <script>
      const ICAL_FEED_URL = "https://calendar.google.com/calendar/ical/marioseixascardosoneto%40gmail.com/public/basic.ics";

      // set text in HTML element "icalFeedUrl" to the URL
      document.getElementById("icalFeedUrl").textContent = ICAL_FEED_URL;

      const copyButton = document.getElementById('copyButton');
      const urlToCopy = ICAL_FEED_URL;

      copyButton.addEventListener('click', () => {
        const tempInput = document.createElement('input');
        tempInput.value = urlToCopy;
        document.body.appendChild(tempInput);
        tempInput.select();
        document.execCommand('copy');
        document.body.removeChild(tempInput);
        alert('URL wurde in die Zwischenablage kopiert!');
      });
    </script>
  </body>
</html>
