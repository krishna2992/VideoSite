
const video = document.getElementById('video');
function initializeVideo() {
}

video.addEventListener('loadedmetadata', initializeVideo);
const resolutionMenu = document.getElementById('resolution-menu');

function changeQualityLevel(hls, newLevel) {
  hls.currentLevel = -1;
  hls.currentLevel = newLevel;
  hls.once(Hls.Events.FRAG_LOADED, function(event, data) {
      hls.startLoad();
      video.play(); 
  });
}

function getLowestResolutionIndex(hls)
{
  var lowestResolutionIndex = 0;
  var lowestResolutionHeight = hls.levels[0].height;
  for (var i = 1; i < hls.levels.length; i++) {
    if (hls.levels[i].height < lowestResolutionHeight) {
        lowestResolutionHeight = hls.levels[i].height;
        lowestResolutionIndex = i;
    }
  }
  return lowestResolutionIndex;
}



function loadVideo() {

  hls = new Hls();
  if (Hls.isSupported()) 
  {
    hls.loadSource('https://demo.unified-streaming.com/k8s/features/stable/video/tears-of-steel/tears-of-steel.ism/.m3u8');
    hls.attachMedia(video);
    hls.on(Hls.Events.MANIFEST_PARSED, function () {
        hls.levels.forEach(function(level, index) {
            var option = document.createElement('option');
            option.text = level.name || `${level.height}p`;
            option.value = index;
            resolutionMenu.appendChild(option);
        });
        setTimeout(function() 
        {
            var index = getLowestResolutionIndex(hls);
            hls.currentLevel = index;
            resolutionMenu.value = index;
        }, 200);
    });
  }
  resolutionMenu.addEventListener('change', function(){
    var selectedResolutionIndex = resolutionMenu.value;
    resolutionMenu.classList.toggle('hidden');
    changeQualityLevel(hls, parseInt(selectedResolutionIndex));
  })
}


// loadVideo();





