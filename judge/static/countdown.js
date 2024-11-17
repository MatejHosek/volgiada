// Set the countdown end
var countdownEnd = document.getElementById("timer").getAttribute("countdownEnd");

var x = setInterval(function() {
  var now = new Date().getTime();

  // Find the distance between now and the count down date
  var distance = countdownEnd - now;

  // Time calculations for hours, minutes and seconds
  var days = Math.floor(distance / (1000 * 60 * 60 * 24));
  var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60)) + days * 24;
  var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
  var seconds = Math.floor((distance % (1000 * 60)) / 1000);

  // Display the timer
  document.getElementById("timer").innerHTML = hours + ":" + minutes + ":" + seconds;

  // If the timer has elapsed, reload the page
  if (distance <= 500) {
    location.reload();
  }
}, 500);