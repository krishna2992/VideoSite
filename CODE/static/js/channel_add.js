class ChannelElement extends HTMLElement
{
    constructor(item)
    {
        super();
        this.profile_picture = item.profile_picture?item.profile_picture:`/static/images/image1.jpg`;
        
        this.innerHTML= `
        <a style="text-decoration: none;" href="/channel/${item.name}" class="video-link" data-source="/static/images/output2.webm">
            <div   class="grid-item-container">
                <div class="grid-item" >
                    <img style="border-radius: 10px;" src="${this.profile_picture}">
                    <div class="overlay">
                        <video  muted loop class="video-preview" style="border-radius: 10px; display: none;"></video>
                    </div>
                </div>
            </div>
            <div  class="info">
                <div   class="name"><p>${capitalize(item.name)}</p></div>
                <div class="views-channel">
                    <div class="views" >${consolidated_views(item.views)} Views</div>
                </div>
            </div>
       </a>`
    }

    

    

    
}


customElements.define('channel-element', ChannelElement);



class NewVideoElement extends HTMLElement
{
    constructor(item)
    {
        
        super();
        console.log(item)
        this.profile = item.profile_picture?item.profile_picture:``;
        this.thumb = item.thumb?item.thumb:``;

        this.innerHTML = `
        <a style="text-decoration: none;" href="/video/${ item.uuid }/${ item.name }" class="video-link" data-source="${this.thumb}">
            <div   class="grid-item-container">
                <div class="grid-item" >
                    <img style="border-radius: 10px;" src="${this.profile}" alt="Item 1">
                    
                        <p style="display:${item.isFull?'block':'none'}"  class="fullContainer">Full Video</p>
                    
                    <p  class="timeDiv" >${secondsToMinute(item.duration)}</p>
                    <div class="overlay">
                        <video  muted loop class="video-preview" style="border-radius: 10px; display: none;"></video>
                    </div>
                </div>
            </div>
            <div  class="info">
                <div   class="name"><p>${capitalize(item.name)}</p></div>
                <div class="views-channel">
                    <div class="views" >${consolidated_views(item.views)} Views</div>
                    <div class="grid-item-channel" >${item.channel.name}</div>
                </div>
            </div>
        </a>`
        
        this.querySelector('.video-link').addEventListener('mouseenter', function() {
            var videoPreview = this.querySelector('.video-preview');
            var videoSource = this.getAttribute('data-source');
            if(videoSource.length!== 0){
                videoPreview.src = videoSource;
                videoPreview.play()
                videoPreview.style.display = 'block';
            }
            
        });
        this.querySelector('.video-link').addEventListener('mouseleave', function() {
            
            var videoPreview = this.querySelector('.video-preview');
            if(videoPreview !== null){
                videoPreview.style.display = 'none';
                videoPreview.pause();
            }
            
        });
        
    }
    

}


class UnUploadedNewVideoElement extends HTMLElement
{
    constructor(item)
    {
        
        super();
        this.profile = item.profile_picture?item.profile_picture:`/static/images/image1.jpg`;
        this.thumb = item.thumb?item.thumb:``;

        this.innerHTML = `
        <div style="text-decoration: none;"  class="video-link" data-source="${this.thumb}">
            <div   class="grid-item-container">
                <div class="grid-item" >
                    <img style="border-radius: 10px;" src="${this.profile}" alt="Item 1">
                    
                        <p style="display:${item.isFull?'block':'none'}"  class="fullContainer">Full Video</p>
                    
                    <p  class="timeDiv" >${secondsToMinute(item.duration)}</p>
                    <div class="overlay">
                        <video  muted loop class="video-preview" style="border-radius: 10px; display: none;"></video>
                    </div>
                </div>
            </div>
            <div  class="info">
                <div   class="name"><p>${capitalize(item.name)}</p></div>
                <div class="views-channel">
                    <div class="grid-item-channel" >${item.channel.name}</div>
                </div>
            </div>
        </div>`
        
        this.querySelector('.video-link').addEventListener('mouseenter', function() {
            var videoPreview = this.querySelector('.video-preview');
            var videoSource = this.getAttribute('data-source');
            if(videoSource.length!== 0){
                videoPreview.src = videoSource;
                videoPreview.play()
                videoPreview.style.display = 'block';
            }
            
        });
        this.querySelector('.video-link').addEventListener('mouseleave', function() {
            
            var videoPreview = this.querySelector('.video-preview');
            if(videoPreview !== null){
                videoPreview.style.display = 'none';
                videoPreview.pause();
            }
            
        });
        
    }
    

}



customElements.define('item-element', NewVideoElement);
customElements.define('unitem-element', UnUploadedNewVideoElement);