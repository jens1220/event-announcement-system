// =====================================
// API GATEWAY URL
// =====================================

const API_URL =
  "https://fn8n8emodd.execute-api.ap-southeast-1.amazonaws.com/prod";


// =====================================
// LOAD EVENTS
// =====================================

async function loadEvents() {

  try {

    const response =
      await fetch("events.json");

    if (!response.ok) {

      throw new Error(
        `Failed to load events.json (${response.status})`
      );
    }

    const events =
      await response.json();

    const container =
      document.getElementById("events");

    container.innerHTML = "";

    if (!events.length) {

      container.innerHTML =
        "<p>No upcoming events.</p>";

      return;
    }

    const event = events[0];

    container.innerHTML = `
      <div class="event-card">
        <h3>${event.title}</h3>
        <p><strong>Date:</strong> ${event.date}</p>
        <p><strong>Time:</strong> ${event.time}</p>
      </div>
    `;

  } catch (error) {

    console.error(
      "Failed to load events:",
      error
    );

    alert(
      "Unable to load events. Check browser console."
    );
  }
}


// =====================================
// SUBSCRIBE USER
// =====================================

async function subscribe() {

  const email =
    document
      .getElementById("email")
      .value
      .trim();

  if (!email) {

    alert(
      "Please enter an email address."
    );

    return;
  }

  try {

    const response = await fetch(
      `${API_URL}/subscribe`,
      {
        method: "POST",

        headers: {
          "Content-Type":
            "application/json"
        },

        body: JSON.stringify({
          email: email
        })
      }
    );

    const data =
      await response.json();

    if (!response.ok) {

      throw new Error(
        data.error ||
        `API Error ${response.status}`
      );
    }

    console.log(
      "Subscription successful:",
      data
    );

    alert(
      data.message ||
      "Subscription request sent successfully."
    );

    document
      .getElementById("email")
      .value = "";

  } catch (error) {

    console.error(
      "Subscription failed:",
      error
    );

    alert(
      error.message ||
      "Subscription failed."
    );
  }
}


// =====================================
// CREATE EVENT
// =====================================

async function createNewEvent() {

  const title =
    document
      .getElementById("title")
      .value
      .trim();

  const date =
    document
      .getElementById("date")
      .value;

  const time =
    document
      .getElementById("time")
      .value;

  if (
    !title ||
    !date ||
    !time
  ) {

    alert(
      "Please complete all event fields."
    );

    return;
  }

  try {

    const response = await fetch(
      `${API_URL}/create-event`,
      {
        method: "POST",

        headers: {
          "Content-Type":
            "application/json"
        },

        body: JSON.stringify({
          title: title,
          date: date,
          time: time
        })
      }
    );

    const data =
      await response.json();

    if (!response.ok) {

      throw new Error(
        data.error ||
        `API Error ${response.status}`
      );
    }

    console.log(
      "Event created:",
      data
    );

    alert(
      data.message ||
      "Event created successfully."
    );

    document
      .getElementById("title")
      .value = "";

    document
      .getElementById("date")
      .value = "";

    document
      .getElementById("time")
      .value = "";

    await loadEvents();

  } catch (error) {

    console.error(
      "Create event failed:",
      error
    );

    alert(
      error.message ||
      "Failed to create event."
    );
  }
}


// =====================================
// INITIAL PAGE LOAD
// =====================================

document.addEventListener(
  "DOMContentLoaded",
  loadEvents
);