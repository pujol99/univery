var DONE_PATH = document.getElementById("popup-done").href;
var UNDONE_PATH = document.getElementById("popup-undone").href;
var DELETE_PATH = document.getElementById("popup-remove").href;
var RESTORE_PATH = document.getElementById("popup-restore").href;

/* Popup open and close method */
var popup = document.getElementById("popup");
popup.style.display = "none";

var closePopupBool = false;
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

// Show colors mouseover detection
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
function openPopup(delivery, next) {
  if(next.includes("calendar") && window.innerWidth < 500){
    window.scrollTo(0, 100);
  }
  var actions = [], blocks = [];
  document.getElementById("popup-done").href = DONE_PATH;
  document.getElementById("popup-undone").href = UNDONE_PATH;
  document.getElementById("popup-remove").href = DELETE_PATH;
  document.getElementById("popup-restore").href = RESTORE_PATH;
  
  document.getElementById("popup").style.display = "block";

  fill_information_popup(
    delivery["name"],
    delivery["description"],
    delivery["toDateStr"],
    delivery["url"],
    delivery["subject_name"]
  );

  clear_actions();
  var next_url = delivery["id"].toString();
  if (next) next_url += "?next=" + next;

  if (delivery["type"] === "Undone") {
    blocks = ["popup-done-div", "popup-remove-div"];
    actions = ["popup-done", "popup-remove"];
  } else if (delivery["type"] === "Done") {
    blocks = ["popup-undone-div", "popup-remove-div"];
    actions = ["popup-undone", "popup-remove"];
  } else if (delivery["type"] === "Removed"){
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
  if(!description){
    document.getElementById("popup-descr").style.display = "none";
  }else{
    document.getElementById("popup-descr").style.display = "block";
    document.getElementById("popup-descr").textContent = description;
  }
  document.getElementById("popup-date").textContent = date;
  document.getElementById("popup-url").href = url;
  document.getElementById("show-url").style.display = url === "None" ? "none" : "block";
  document.getElementById("popup-subject").textContent = subject;
}

function clear_actions(){
  //Clear delivery options
  document.getElementById("popup-done-div").style.display = "none";
  document.getElementById("popup-undone-div").style.display = "none";
  document.getElementById("popup-remove-div").style.display = "none";
  document.getElementById("popup-restore-div").style.display = "none";
}