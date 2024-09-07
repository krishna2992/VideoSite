

var timeDivs = document.querySelectorAll('.timeDiv');
timeDivs.forEach(function(div){
    var seconds = parseInt(div.getAttribute('data-seconds'));
    div.innerText = secondsToMinute(seconds);
})

var nameDivs = document.querySelectorAll('.name');
nameDivs.forEach(function(div){
    var name = div.getAttribute('data-name');
    div.innerText = capitalize(name);
})

var viewDivs = document.querySelectorAll('.views');
viewDivs.forEach(function(div){
    var value = parseInt(div.getAttribute('data-views'));
    div.innerText  = consolidated_views(value)+' Views';
})
