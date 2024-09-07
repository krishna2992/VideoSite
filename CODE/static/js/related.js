var itemName = document.getElementById('item-name');
var value = itemName.getAttribute('data-name');
itemName.innerText = capitalize(value);
var itemViews = document.getElementById('item-views');
var value = parseInt(itemViews.getAttribute('data-views'));
itemViews.innerText = consolidated_views(value);




var gridMainContainer = document.getElementById('gridMainContainer');
var videocontainer = document.getElementById('video-container');
var loadButton = document.getElementById('loadMore');
async function get_more(page=2)
{
    var uuid = videocontainer.getAttribute('data-id');
    var name = videocontainer.getAttribute('data-name');
    const items = await fetch(`/endpoint/related/${uuid}/${name}?page=${page}`)
    return items.json();
}
async function loadMore()
{
    
    var div = document.createElement('div');
    div.className = 'add-div';
    div.innerText = 'Add Container';
    gridMainContainer.append(div);
    var items = await get_more(parseInt(loadButton.getAttribute('data-current'))+1);
    console.log(items)
    if(items.length!==0)
    {
        var div = document.createElement('div');
        div.className = 'grid-container';
        items.forEach(item=>{
            div.append(new NewVideoElement(item))
        })
        gridMainContainer.appendChild(div);
    
    }
    
}




if(parseInt(loadButton.getAttribute('data-pages')) === 1)
{
    loadButton.disabled= true;
    loadButton.style.display= 'none';
}
else{
    loadButton.addEventListener('click',  async function()
    {
        var current = parseInt(loadButton.getAttribute('data-current'));
        var total = parseInt(loadButton.getAttribute('data-pages'));
        await loadMore();
        loadButton.setAttribute('data-current', current+1);
        if(current+1 === 3)
        {
            loadButton.disabled = true;
            loadButton.style.display = 'none';
        }
    })
}
