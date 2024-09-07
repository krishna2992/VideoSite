var videoLinks = document.querySelectorAll('.video-link');
                videoLinks.forEach(function(videoLink) {
                videoLink.addEventListener('mouseenter', function() {
                    
                    var videoPreview = this.querySelector('.video-preview');
                    if(videoPreview !== null)
                    {
                        var videoSource = this.getAttribute('data-source');
                        if(videoSource.length!== 0){
                            videoPreview.src = videoSource;
                            videoPreview.play()
                            videoPreview.style.display = 'block';
                        }
                    }
                    
                });
                videoLink.addEventListener('mouseleave', function() {
                    
                    var videoPreview = this.querySelector('.video-preview');
                    if(videoPreview!==null)
                    {
                        if(videoPreview.src !== null){
                            videoPreview.style.display = 'none';
                            videoPreview.pause();
                        }
                    }
                    
                    
                });
            });