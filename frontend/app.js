fetch("events.json")
  .then(response => response.json())
  .then(events => {

    const container =
      document.getElementById("events");

    container.innerHTML = "";

    events.forEach(event => {

      container.innerHTML += `
        <div class="event-card">
          <h3>${event.title}</h3>
          <p>Date: ${event.date}</p>
          <p>Time: ${event.time}</p>
        </div>
      `;
    });

  })
  .catch(error => {
    console.error(
      "Failed to load events:",
      error
    );
  });

async function subscribe() {

  const email =
    document.getElementById("email").value;

  if (!email) {
    alert("Please enter an email.");
    return;
  }

  try {

    const response = await fetch(
      "https://abc123.execute-api.ap-southeast-1.amazonaws.com/prod/subscribe",
      {
        method: "POST",

        headers: {
          "Content-Type":
            "application/json"
        },

        body: JSON.stringify({
          email
        })
      }
    );

    const data =
      await response.json();

    alert(data.message);

  } catch (error) {

    console.error(error);

    alert(
      "Subscription failed."
    );
  }
}

async function createEvent() {

  const title =
    document.getElementById("title").value;

  const date =
    document.getElementById("date").value;

  const time =
    document.getElementById("time").value;

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
      "https://abc123.execute-api.ap-southeast-1.amazonaws.com/prod/create-event",
      {
        method: "POST",

        headers: {
          "Content-Type":
            "application/json"
        },

        body: JSON.stringify({
          title,
          date,
          time
        })
      }
    );

    const data =
      await response.json();

    alert(data.message);

  } catch (error) {

    console.error(error);

    alert(
      "Failed to create event."
    );
  }
}