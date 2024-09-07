document.addEventListener('DOMContentLoaded', function() {
    const downloadButton = document.getElementById('downloadButton');
    const progressBar = document.getElementById('progressBar');
    
    downloadButton.addEventListener('click', function() {
      downloadFile(videoPlayer.src);
    });
  
    function downloadFile(url) {
      const xhr = new XMLHttpRequest();
      xhr.open('GET', url, true);
      xhr.responseType = 'blob'; // Use 'blob' for binary data
      xhr.onload = function() {
        if (xhr.status === 200) {
          const blob = xhr.response;
          const filename = data.item.name+'.mp4'; // You can extract filename from response headers if needed
          const a = document.createElement('a');
          a.href = window.URL.createObjectURL(blob);
          a.download = filename;
          document.body.appendChild(a);
          a.click();
          document.body.removeChild(a);
        }
      };
      
      xhr.onprogress = function(e) {
        if (e.lengthComputable) {
          const percentComplete = (e.loaded / e.total) * 100;
          progressBar.style.width = percentComplete + '%';
        }
      };
      
      xhr.send();
    }
  });