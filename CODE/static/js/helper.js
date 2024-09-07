function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Check if this cookie string begins with the name we want
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function secondsToMinute(seconds)
{
    var hour = Math.floor(seconds/3600);
    var minute =Math.floor((seconds%3600)/60);
    var seconds  = Math.floor(seconds%60);
    var timStr = ''
    if(hour>0){
        if(hour < 10)
        {
            timStr+='0';
        }
        timStr+= hour+':'
    }
    if(minute<10)
    {
        timStr+='0';
    }
    
    timStr+=minute+':';
    if(seconds<10)
    {
        timStr+='0';
    }
    timStr+=seconds;
    return timStr;
}

function capitalize(value)
{
    var parts = value.split(" ");
    for(var i = 0; i < parts.length; i++)
    {
        parts[i] = parts[i].charAt(0).toUpperCase()+parts[i].slice(1);
    }
    return parts.join(" ");
}

function consolidated_views(value)
{   
    if (value >= 1000000)
    {
        return (value/1000000).toFixed(2)+' M';
    }
    else if(value >= 1000)
    {
        return (value/1000).toFixed(2)+' K';
    }
    else{
        return value;
    }
}


function addToGrid(items, gridElement)
{
    
    if(items.length === 0)
    {
        gridElement.innerHTML = '<p class="empty-grid" >No  Videos Found</p>';
    }
    else{
        gridElement.innerHTML = '';
        items.forEach(item=>{
            var cus = new NewVideoElement(item);
            gridElement.append(cus);
        })
    }
    
}


function toggleMenu() 
{
    
    var sidebar = document.getElementById("sidebar");
    var menuToggle = document.getElementById("menuToggle");
    sidebar.classList.toggle("open");
    menuToggle.classList.toggle("active"); // Add or remove "active" class
}
function closeMenuOnClickOutside(event) 
{
    var sidebar = document.getElementById("sidebar");
    var menuToggle = document.getElementById("menuToggle");
    if (!sidebar.contains(event.target) && !menuToggle.contains(event.target)) {
        sidebar.classList.remove("open");
        menuToggle.classList.remove("active");
    }
}


function setCookie(name, value, daysToLive) {
    var cookie = name + '=' + value;
    if (typeof daysToLive === 'number') {
        cookie += '; max-age=' + (daysToLive * 24 * 60 * 60);
    }
    document.cookie = cookie;
}
document.addEventListener("click", closeMenuOnClickOutside);


function myFunction()
{
    var password = document.getElementById('id_password');
    if(password.type == 'password')
    {
        password.type = 'text';
    }
    else{
        password.type = 'password';
    }
}

function dataURLtoBlob(dataURL) {
    const [header, data] = dataURL.split(',');
    const mime = header.match(/:(.*?);/)[1];
    const binary = atob(data);
    const array = [];
    for (let i = 0; i < binary.length; i++) {
        array.push(binary.charCodeAt(i));
    }
    return new Blob([new Uint8Array(array)], { type: mime });
}