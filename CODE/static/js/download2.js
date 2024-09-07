document.addEventListener('DOMContentLoaded', function() {
    const downloadButton = document.getElementById('downloadButton');
    
    downloadButton.addEventListener('click', function() {
        var location = window.location;
        window.location = `/user/login?next=${location}`
    });
  });