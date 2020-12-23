var items = [].slice.call(document.getElementsByClassName("time"));

var toDates = [];
items.forEach((item) => toDates.push(new Date(item.textContent).getTime()));

function computeTime() {
  items.forEach(function (item, i) {
    var now = new Date().getTime();
    var distance = toDates[i] - now;

    var days = Math.floor(distance / (1000 * 60 * 60 * 24));
    var hours = Math.floor(
      (distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60)
    );
    var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
    var seconds = Math.floor((distance % (1000 * 60)) / 1000);
    
    if(days < 0){
      item.textContent = days + "d " + hours + "h " + minutes + "m ";
    }else if (days < 1){
      item.textContent = hours + "h " + minutes + "m ";
    }else{
      item.textContent = days + "d " + hours + "h ";
    }
    
  });
}

computeTime();
setInterval(computeTime, 1000);

