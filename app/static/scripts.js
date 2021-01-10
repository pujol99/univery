var TODO_DATES_CONTENT = [].slice.call(document.getElementsByClassName("time"));
var TODO_DATES = [];
TODO_DATES_CONTENT.forEach((item) =>
  TODO_DATES.push(new Date(item.textContent).getTime())
);
var DONE_PATH = document.getElementById("popup-done").href;
var UNDONE_PATH = document.getElementById("popup-undone").href;
var DELETE_PATH = document.getElementById("popup-delete").href;
var RESTORE_PATH = document.getElementById("popup-restore").href;

/* Compute time to each delivery in real time */
function computeTime() {
  
  TODO_DATES_CONTENT.forEach(function (item, i) {
    var now = new Date().getTime();
    var distance = TODO_DATES[i] - now;

    var days = Math.floor(distance / (1000 * 60 * 60 * 24));
    var hours = Math.floor(
      (distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));

    if (days < 0) {
      item.textContent = days + "d " + hours + "h " + minutes + "m ";
    } else if (days < 1) {
      item.textContent = hours + "h " + minutes + "m ";
    } else {
      item.textContent = days + "d " + hours + "h ";
    }
  });
}
computeTime();
setInterval(computeTime, 1000);


/* Change page as dropdown value change */
function deliveryType() {
  
  var dropdown_value = document.getElementById("delivery-type").value;
  window.location = dropdown_value;
}

/* Popup open and close method */
var popup = document.getElementById("popup");
var closePopupBool = false;
popup.style.display = "none";

$(function () {
  $("body").click(function (e) {
    if (popup.style.display === "block") {
      if (!(e.target.id == "popup" || $(e.target).parents("#popup").length)) {
        if (closePopupBool) {
          popup.style.display = "none";
          closePopupBool = false;
        } else {
          closePopupBool = true;
        }}}
  });
});

/* Waiting Loading state of button */
var waitin = document.getElementById("waiting");
var loadin = document.getElementById("loading");

loadin.style.display = "none";

document.getElementById("refresh-text").onclick = function () {
  waitin.style.display = "none";
  loadin.style.display = "block";
};

/* Random HEX color picker */
function randomColor() {
  var color = document.getElementById("color-content");

  color.value = Math.floor(Math.random() * 16777215).toString(16);
  color.style.backgroundColor = color.value;
}

/* Show colors mouseover detection */
var popupColor = document.getElementById("popup-colors");
var popupColorTrigger = document.getElementById("colors-btn");

popupColor.style.display = "none";

popupColorTrigger.onmouseover = function () {
  popupColor.style.display = "block";
};
popupColorTrigger.onmouseout = function () {
  popupColor.style.display = "none";
};

/* Delivery popup information */
function openPopup(delivery, next, ) {
  var actions = [], blocks = [];
  document.getElementById("popup-done").href = DONE_PATH;
  document.getElementById("popup-undone").href = UNDONE_PATH;
  document.getElementById("popup-delete").href = DELETE_PATH;
  document.getElementById("popup-restore").href = RESTORE_PATH;
  
  document.getElementById("popup").style.display = "block";

  fill_information_popup(
    delivery[0],
    delivery[1].replaceAll("~", "\n"),
    delivery[2],
    delivery[3],
    delivery[5]
  );

  clear_actions();
  console.log(next);
  var next_url = delivery[7].toString();
  if (next) {
    next_url += "?next=" + next;
  } 

  if (delivery[4] === "Done") {
    blocks = ["popup-done-div", "popup-delete-div"];
    actions = ["popup-done", "popup-delete"];
  } 
  else if (delivery[4] === "Undone") {
    blocks = ["popup-undone-div", "popup-delete-div"];
    actions = ["popup-undone", "popup-delete"];
  } 
  else if (delivery[4] === "Restore"){
    blocks = ["popup-restore-div"];
    actions = ["popup-restore"];
  }

  for (i = 0; i < blocks.length; i++)
    document.getElementById(blocks[i]).style.display = "block";
    
  for (i = 0; i < actions.length; i++) {
    var textDone = document.getElementById(actions[i]).href;
    var textDoneID = textDone.slice(0, textDone.length - 1) + next_url;
    document.getElementById(actions[i]).href = textDoneID;
  }
}

function fill_information_popup(name, description, date, url, subject){
  document.getElementById("popup-name").textContent = name;
  document.getElementById("popup-descr").textContent = description;
  document.getElementById("popup-date").textContent = date;
  document.getElementById("popup-url").href = url;
  document.getElementById("show-url").style.display =
    url === "None" ? "none" : "block";
  document.getElementById("popup-subject").textContent = subject;
}

function clear_actions(){
  //Clear delivery options
  document.getElementById("popup-done-div").style.display = "none";
  document.getElementById("popup-undone-div").style.display = "none";
  document.getElementById("popup-delete-div").style.display = "none";
  document.getElementById("popup-restore-div").style.display = "none";
}

