// script.js

function getLocation() {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (pos) => {
          document.getElementById("location").innerText = `Location: ${pos.coords.latitude}, ${pos.coords.longitude}`;
        },
        (err) => {
          document.getElementById("location").innerText = "Unable to retrieve location";
        }
      );
    } else {
      document.getElementById("location").innerText = "Geolocation not supported";
    }
  }
  
  function sendSOS() {
    alert("SOS Sent! Authorities Notified.");
  }
  
  // Run getLocation only if the element exists on the page
  document.addEventListener("DOMContentLoaded", () => {
    if (document.getElementById("location")) {
      getLocation();
    }
  });
  

  function searchRoad() {
    const roadName = document.getElementById("roadSearch").value;
    const safetyRatingElement = document.getElementById("safetyRating");

    if (roadName.trim() === "") {
        safetyRatingElement.innerText = "Safety Rating: Please enter a road name.";
        return;
    }

    // In a real application, you would fetch the safety rating from a database or API.
    // This is a placeholder.
    const safetyRating = getSafetyRating(roadName); // Replace with your actual data fetching

    if (safetyRating) {
        safetyRatingElement.innerText = `Safety Rating: ${safetyRating}`;
    } else {
        safetyRatingElement.innerText = "Safety Rating: Road not found.";
    }
}

// Placeholder function - Replace with your actual data retrieval logic
function getSafetyRating(roadName) {
    // In a real application, you would query a database or API.
    // This is just sample data.
    const roadSafetyData = {
        "Main Street": "A+",
        "First Avenue": "B",
        "Highway 101": "C-",
        "Unknown Road": null // Example of a road not found
    };

    return roadSafetyData[roadName]; // Returns the rating or undefined if not found
}

// Sample SOS notifications (replace with your actual data fetching)
const sosNotifications = document.getElementById("sosNotifications");

// Placeholder for fetching notifications - replace with your actual logic
function fetchSOSNotifications() {
    // In a real app, you would fetch this from a server.
    const sampleNotifications = [
        { message: "SOS from User 1. Location: 12.9716, 79.1581" },
        { message: "SOS from User 2. Location: 13.0827, 80.2707" },
        { message: "SOS from User 3. Location: 11.0050, 76.9833" }
    ];

    sampleNotifications.forEach(notification => {
        const sosMessageDiv = document.createElement("div");
        sosMessageDiv.className = "sos-message";
        sosMessageDiv.textContent = notification.message;
        sosNotifications.appendChild(sosMessageDiv);
    });
}

document.addEventListener("DOMContentLoaded", () => {
    fetchSOSNotifications(); // Fetch notifications when the page loads
});

document.addEventListener('DOMContentLoaded', () => {
  const themeToggle = document.getElementById('theme-toggle');
  const body = document.body;

  // 🌙 Check user preference
  const prefersDarkMode = window.matchMedia('(prefers-color-scheme: dark)').matches;
  const currentTheme = localStorage.getItem('theme') || (prefersDarkMode ? 'dark' : 'light');
  
  body.classList.toggle('dark', currentTheme === 'dark');
  themeToggle.textContent = currentTheme === 'dark' ? '☀️' : '🌙';

  // 🔘 Toggle theme
  themeToggle.addEventListener('click', () => {
      const isDark = body.classList.toggle('dark');
      localStorage.setItem('theme', isDark ? 'dark' : 'light');
      themeToggle.textContent = isDark ? '☀️' : '🌙';
  });
});
