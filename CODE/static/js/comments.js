var submitButton = document.getElementById('submitButton');
if(submitButton)
{
  const inputElement = document.getElementById('commentInput');
  submitButton.addEventListener('click', async function(){
      const content = inputElement.value;
      if(!content || content === '')
      {
        alert('Empty Comment');
        return;
      }
      await submitComment(content);
      inputElement.value = '';
  })
}
// Define a class that extends HTMLElement
class UserCard extends HTMLElement {
    constructor(name, content, replys) {
      super(); // Always call super() first in the constructor
      const res = replys.length>0?'block':'none';
      let divs = ''
      for(var i = 0; i < replys.length; i++)
      {
        divs+= `<div class="comment" style="">
            <div class="comment-user" style="">
                <div class="comment-avatar" style=""></div>
        
            </div>
            <p style="margin:0px 2px;font-size:14px;">${replys[i].content ||''}</p></div>`
      }
      // Define the HTML structure using innerHTML
      this.innerHTML = `   
    <div  class="comment" >
        <div class="comment-user" >
            <div class="comment-avatar" ></div>
            <h4 class="comment-user" style="margin:0;">${name || 'Unknown'}</h4>
        </div>
        <p style="margin:0px 2px;font-size:12px;">${content ||''}</p>
        <div class="shadow-replys" style='margin-left:100px;display:none;' class='replys'>${divs}</div>
        <div class="view-replies" style="font-size: 18px; margin-left: 100px; padding: 5px; cursor: pointer;display:${res};"
                    >View Replies</div>
    </div>`;

        const viewRepliesButton = this.querySelector('.view-replies');
        
        // Toggle replies visibility function
        const toggleReplies = () => {
            const replyDiv = this.shadowRoot.querySelector('.shadow-replys');
            if (replyDiv.style.display === 'none') {
                replyDiv.style.display = 'block';
                viewRepliesButton.textContent = 'Hide Replies';
            } else {
                replyDiv.style.display = 'none';
                viewRepliesButton.textContent = 'View Replies';
            }
        };

        // Bind the toggleReplies function to click event of viewRepliesButton
        viewRepliesButton.addEventListener('click', toggleReplies);
    }  
  }

  customElements.define('user-card', UserCard);
  function createCards(comments) 
  {
    
    const targetDiv = document.getElementById('commentBox');
    targetDiv.innerHTML = '';
    for (let i = 0; i < comments.length; i++) 
    {
      
      const name = comments[i].user;
      const content = comments[i].content;
      const userCard = new UserCard(name, content,[]);
      targetDiv.appendChild(userCard);
    }
  }

  const protocol = window.location.protocol;
  const hostname = window.location.hostname;
  const port = window.location.port;
  


var commentBox = document.getElementById('commentBox');
var commentButton = document.getElementById('commentButton');
var commentContainer = document.getElementById('commentContainer');
var commentCount = document.getElementById('commentCount');
commentCount.innerText = data.item.comment_count;
commentButton.addEventListener('click', async function(){

    if(commentContainer.style.display == 'block')
    {
      return;
    }
    var itemId = data.item.id;
    try{
        const newUrl = `${protocol}//${hostname}${port ? ':' + port : ''}/api/comments/${itemId}?page=${1}`;            
        const responce = await fetch(newUrl);

        if(!responce.ok)
        {
            console.log(responce)
            throw new Error('Network response was not ok');
        }
        const data = await responce.json();
        createCards(data);
        // commentBox.setAttribute('data-page', 1);
        commentContainer.style.display='block';
      } 
      catch (error) {
        console.error('Error fetching data:', error);
      }
})
  
async function comment_page(page_n)
{
    var itemId = data.item.id;
    try{
        const newUrl = `${protocol}//${hostname}${port ? ':' + port : ''}/api/comments/${itemId}?page=${page_n}`;            
        const responce = await fetch(newUrl);

        if(!responce.ok)
        { 
            console.log(responce)
            throw new Error('Network response was not ok');
        }
        const data = await responce.json();
        createCards(data);
        commentBox.setAttribute('data-page', page_n)
      } 
      catch (error) {
        console.error('Error fetching data:', error);
      }
}

var nextButton = document.getElementById('nextPage')
nextButton.addEventListener('click', async function()
{
  var boxContainer = document.getElementById('pageBoxContainer');
  const l = parseInt(boxContainer.getAttribute('data-length'));
  var current = parseInt(commentBox.getAttribute('data-page'));
  
  if(current===l)
  {
    
    return;
  }
  if(current%5 === 0)
  {
    boxContainer.innerHTML = '';
    var m = l<current+5?l:current+5;
    for(var i=current+1; i<=m; i++)
    {
      var div = document.createElement('div');
      div.className = 'page-num';
      div.innerText = i;
      div.setAttribute('data-page', i);
      div.addEventListener('click', function(){
          comment_page(parseInt(this.getAttribute('data-page')));
      })
      boxContainer.appendChild(div);
    }
  }
  var itemId = data.item.id;
    try{
        const newUrl = `${protocol}//${hostname}${port ? ':' + port : ''}/api/comments/${itemId}?page=${current+1}`;            
        const responce = await fetch(newUrl);

        if(!responce.ok)
        { 
            console.log(responce)
            throw new Error('Network response was not ok');
        }
        const data = await responce.json();
        
        createCards(data);
        commentBox.setAttribute('data-page', current+1);
      } 
      catch (error) {
        console.error('Error fetching data:', error);
      }
})

var prevButton = document.getElementById('prevPage')
prevButton.addEventListener('click', async function(){
  var current = parseInt(commentBox.getAttribute('data-page'));
  if(current===1)
  {
    return;
  }
  if(current%5 === 1)
  {
    boxContainer.innerHTML = '';
    // var m = current-5?l:current+5;
    for(var i=current-5; i<current; i++)
    {
      var div = document.createElement('div');
      div.className = 'page-num';
      div.innerText = i;
      div.setAttribute('data-page', i);
      div.addEventListener('click', function(){
          comment_page(parseInt(this.getAttribute('data-page')));
      })
      boxContainer.appendChild(div);
    }
  }
  var itemId = data.item.id;
    try{
        const newUrl = `${protocol}//${hostname}${port ? ':' + port : ''}/api/comments/${itemId}?page=${current-1}`;            
        const responce = await fetch(newUrl);

        if(!responce.ok)
        { 
            console.log(responce)
            throw new Error('Network response was not ok');
        }
        const data = await responce.json();
        createCards(data);
        commentBox.setAttribute('data-page', current-1);
      } 
      catch (error) {
        console.error('Error fetching data:', error);
      }
})


async function goto_page(target)
{
  var itemId = data.item.id;
    try{
        const newUrl = `${protocol}//${hostname}${port ? ':' + port : ''}/api/comments/${itemId}?page=${target}`;            
        const responce = await fetch(newUrl);

        if(!responce.ok)
        { 
            console.log(responce)
            throw new Error('Network response was not ok');
        }
        const data = await responce.json();
        createCards(data);
        commentBox.setAttribute('data-page', target);
      } 
      catch (error) {
        console.error('Error fetching data:', error);
      } 
}

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


async function submitComment(content)
{
  var itemId = data.item.id;
  const newUrl = `${protocol}//${hostname}${port ? ':' + port : ''}/post/comments/${itemId}`;            

  

const formData = new FormData();
formData.append('content', content);


const options = {
    method: 'POST',
    headers: {
        // 'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken')
  
    },
    body: formData
};

fetch(newUrl, options)
    .then(response => response.json())
    .then(data => {
      
      const userCard = new UserCard(data.username, data.content, []);
      commentBox.insertBefore(userCard, commentBox.firstChild);
      commentCount.innerText = parseInt(commentCount.innerText)+1;
    })
    .catch((error) => {
        console.error('Error:', error);
        return 400;
    }); 
}


async function addToFavourite()
{
  var itemId = data.item.id;
  const newUrl = `${protocol}//${hostname}${port ? ':' + port : ''}/vide/favourite/${itemId}`;            


const formData = new FormData();

const options = {
    method: 'POST',
    headers: {
        // 'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken')
  
    },
    body: formData
};

fetch(newUrl, options)
    .then(response => response.json())
    .then(data => {
      
      const userCard = new UserCard(data.username, data.content, []);
      commentBox.insertBefore(userCard, commentBox.firstChild);
      commentCount.innerText = parseInt(commentCount.innerText)+1;
    })
    .catch((error) => {
        console.error('Error:', error);
        return 400;
    }); 
}


var boxContainer = document.getElementById('pageBoxContainer');
const l = parseInt(boxContainer.getAttribute('data-length'));
if(l!==0)
{
    var minimum = l<5?l:5;
    for(var i= 0; i < minimum; i++)
    {
        var div = document.createElement('div');
        div.className = 'page-num';
        div.innerText = i+1;
        div.setAttribute('data-page', i+1);
        div.addEventListener('click', function(){
        comment_page(parseInt(this.getAttribute('data-page')));
        })
        boxContainer.appendChild(div);
    }

}
else{
    document.getElementById('prevPage').style.display = 'none';
    document.getElementById('nextPage').style.display = 'none';
}