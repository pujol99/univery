var TODO_DATES_CONTENT = [].slice.call(document.getElementsByClassName("time"));
var TODO_DATES = [];
TODO_DATES_CONTENT.forEach((item) =>
  TODO_DATES.push(new Date(item.textContent).getTime())
);

/* Compute time to each delivery in real time */
function computeTime() {
  
  TODO_DATES_CONTENT.forEach(function (item, i) {
    var now = new Date().getTime();
    var distance = TODO_DATES[i] - now;

    var days = Math.floor(distance / (1000 * 60 * 60 * 24));
    var hours = Math.floor(
      (distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));

    if (days < 1) {
      item.textContent = hours + "h " + minutes + "m ";
    } else {
      item.textContent = days + "d " + hours + "h ";
    }
  });
}
computeTime();
setInterval(computeTime, 1000);

/* Random HEX color picker */
function randomColor() {
  var color = document.getElementById("color-content");

  color.value = ((Math.random() * 0xffffff) << 0).toString(16).padStart(6, "0");
  color.style.backgroundColor = color.value;
}

// Copy paste ID
function setSubject(element) {
  clear_subjects_bg()
  element.style.backgroundColor = "black";
  element.style.color = "white";
  document.getElementById("subjectID").value = element.getAttribute("value");
  document.getElementById("subjectID").style.backgroundColor = "#000";
  document.getElementById("subjectID").style.color = "#fff";

  randomColor();

  document.getElementById("hideColor").style.visibility = "visible";
  document.getElementById("hideColor").style.opacity = "1";
}

function clear_subjects_bg(){
  var list = document.getElementsByClassName("clear");
  for (let item of list) {
    item.style.backgroundColor = "white";
    item.style.color = "black";
  }
}

// Change icon to loading
var loaders = document.getElementsByClassName("loading-icon");
for (let item of loaders) {
  item.style.display = "none";
}

function toLoading() {
  var bloaders = document.getElementsByClassName('bloading');
  var loaders = document.getElementsByClassName('loading-icon');

  for (let item of bloaders) {
    item.style.display = "none";
  }
  for (let item of loaders) {
    item.style.display = "inline-block";
  }
}