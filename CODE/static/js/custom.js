var gridMainContainer = document.getElementById('gridMainContainer');
        
var loadButton = document.getElementById('loadMore');
if(data.items.length !== 0)
{
    var div = document.createElement('div');
    div.className = 'grid-container';
    data.items.forEach(i=>{
        i.isFull = JSON.parse(i.isFull);
        div.append(new NewVideoElement(i))
    })
    gridMainContainer.appendChild(div);
    
}
async function get_more(page=2)
{
    var uuid = data.item.uuid;
    var name = data.item.name;
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
else
{
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