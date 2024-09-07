var favButton = document.getElementById('favButton');   
function addToFavorites() 
{
    
    const apiUrl = '/api/favourite/video';

    // Assuming you are authenticated and have CSRF token if required
    const csrftoken = getCookie('csrftoken');  // Function to get CSRF token

    fetch(apiUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({ video_id:  data.item['id'] }),
    })
    .then(response => {
        if (!response.ok) {
            if(response.status === 403)
            {
                window.location.href = `/user/login?next=${window.location.pathname + window.location.search + window.location.hash}`;    
            }
            
        }
        return response.status;
    })
    .then(res => {
        if(res === 201)
        {   favButton.textContent = 'Remove from Fav';
            
        }
        else{
            favButton.textContent= 'Add To Fav';
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}


var itemName = document.getElementById('item-name');
itemName.innerText = capitalize(data.item.name);
var itemViews = document.getElementById('item-views');
itemViews.innerText = consolidated_views(data.item.views);
        
var tagContainer =     document.getElementById('tagContainer');
var channelContainer = document.getElementById('channelContainer');
channelContainer.innerHTML = `<a  href="/channel/${ data.item.channel.name }" >
        ${ data.item.channel.name }<span class="tag channel-views">${consolidated_views(Math.max(1020, data.item.channel.subscribers_count))}</span>
    </a>`
var actors = data.item['actors'];
var tags = data.item['tags'];
actors.forEach(actor=>{
    var a = document.createElement('a');
    a.style.display='flex';
    var img = document.createElement('img')
    var p = document.createElement('p')
    img.src = "/static/images/person.svg";
    img.style.width = '15px';
    p.textContent = capitalize(actor.name);
    a.appendChild(img)
    a.appendChild(p)
    a.href = `/actor/${actor.name}`;
    a.className='tag';
    tagContainer.append(a);
})
tags.forEach(tag=>{
    var a = document.createElement('a');
    a.href = `/tag/${tag.name}`;
    a.className='tag';
    a.textContent = capitalize(tag.name);
    tagContainer.append(a);
})
    
    var resolutionSelect = document.getElementById('resolutionSelect');
    let effectiveConnectionType = '4g'; // Default to 4G if API is not supported
    const videoPlayer = document.getElementById('video');
    videoPlayer.poster = data.item.profile_picture;
    data.item.resolutions.forEach(res=>{
        var option = document.createElement('option');
        option.value = res.video;
        option.textContent = res.resolution;
        resolutionSelect.appendChild(option);
    })

    if (navigator.connection && navigator.connection.effectiveType) {
        effectiveConnectionType = navigator.connection.effectiveType;
    }

    let selectedSource;
    var options = resolutionSelect.getElementsByTagName('option')
    
    

    if (effectiveConnectionType === '4g') {
        for(var i =0; i<options.length; i++)
        {
            if(options[i].textContent === '480p')
            {
                selectedSource = options[i];
                break;
            }
        }
        // selectedSource = options.find(option => option.textContent === '480p');
    } else if (effectiveConnectionType === '3g') {
        for(var i =0; i<options.length; i++)
        {
            if(options[i].textContent === '360p')
            {
                selectedSource = options[i];
                break;
            }
        }
    } else {
        for(var i =0; i<options.length; i++)
        {
            if(options[i].textContent === '240p')
            {
                selectedSource = options[i];
                break;
            }
        }
    }
    if(!selectedSource)
    {
        selectedSource = options[0];
    }
    
    videoPlayer.src = selectedSource.value;
    videoPlayer.load();
                
                
    resolutionSelect.addEventListener('change', function(){
        const selectedVideo = resolutionSelect.value;
        videoPlayer.pause()
        videoPlayer.src = selectedVideo;
        videoPlayer.load(); // Reload the video element to apply changes
        videoPlayer.play()
    })


// const videoPlayer = document.getElementById('video');
const videoSource = document.getElementById('videoSource');
// const resolutionSelect = document.getElementById('resolutionSelect');

function hideResolutionSelect() {
resolutionSelect.style.display = 'none';
}

function showResolutionSelect() {
resolutionSelect.style.display = 'block';
}

function changeResolution(resolution) {
// Update video source based on selected resolution
videoSource.src = `example_${resolution}.mp4`;
videoPlayer.load(); // Reload the video element to apply the new source
videoPlayer.play(); // Start playing the video with the new source
}
function hideControls() {
// Hide controls when the video is paused
if (videoPlayer.paused) {
    videoPlayer.controls = false;
} else {
    videoPlayer.controls = true;
}
}

const playButton = document.getElementById('playButton');
const videoContainer = document.getElementById('videoContainer');

// Initially show the play button
playButton.style.display = 'block';

videoPlayer.addEventListener('play', () => {
playButton.style.display = 'none';
hideResolutionSelect();
hideControls();
});

videoPlayer.addEventListener('pause', () => {
playButton.style.display = 'block';
showResolutionSelect();
hideControls();
});

function playVideo() {
    videoPlayer.play();
}

videoPlayer.addEventListener('contextmenu', function(event){

    event.preventDefault(); // Prevent the default context menu
    customMenu.style.display = 'block'; // Show the custom context menu
    customMenu.style.left = `${event.pageX}px`; // Position menu horizontally
    customMenu.style.top = `${event.pageY}px`;
})

var customMenuElements = document.querySelectorAll('.customMenuElement');
customMenuElements.forEach(ele=>{
    ele.addEventListener('contextmenu', function(event){
        event.preventDefault();
    })
})

document.addEventListener('DOMContentLoaded', () => {
    const menu = document.getElementById('customMenu');
    document.addEventListener('click', (e) => {
        if (!menu.contains(e.target)) {
            menu.style.display = 'none';
        }
    });
});