// Set the countdown end
var countdownEnd = document.getElementById("timer").getAttribute("countdownEnd");
var lastReload = null;

function updateTimer() {
  var now = new Date().getTime();

  // Find the distance between now and the count down date
  var distance = countdownEnd - now;

  // Set the lastReload for reloading mid-competition
  if (lastReload == null) {
    lastReload = now;
  }

  // Time calculations for hours, minutes and seconds
  var days = Math.floor(distance / (1000 * 60 * 60 * 24));
  var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60)) + days * 24;
  var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
  var seconds = Math.floor((distance % (1000 * 60)) / 1000);

  // Display the timer
  document.getElementById("timer").innerHTML = (
    ('0' + Math.max(0, hours)).slice(-Math.max(2, hours.toString().length)) + ":" + 
    ('0' + Math.max(0, minutes)).slice(-2) + ":" + 
    ('0' + Math.max(0, seconds)).slice(-2)
  );

  // If the timer has elapsed, reload the page
  if (distance <= 0 || lastReload + 10000 < now) {
    lastReload = now;
    location.reload();
  }
}

updateTimer();
var x = setInterval(function() {
  updateTimer();
}, 500);