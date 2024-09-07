
document.addEventListener('DOMContentLoaded', async function(){
    var pagenavigatorcontainer= document.querySelector('.page-navigator-container');
    var listedContainer = document.querySelector('.listed');
    var itemsPageContainer = document.getElementById('itempageBoxContainer')    
    var current = parseInt(itemsPageContainer.getAttribute('data-page'));
    var total = parseInt(itemsPageContainer.getAttribute('data-length'));
    var prevItemsPage = document.getElementById('prevItemsPage');
    var nextItemsPage = document.getElementById('nextItemsPage');
    
function upDate_Nav(c)
{
    if(c%5 === 0)
    {
        var a = c-5+1;
    }
    else{
        var a =c- c%5+1;
    }
    var b  = (a+5-1)<total?a+5-1:total;
    itemsPageContainer.innerHTML = '';
    for(var i= a; i <= b; i++)
    {
        var div = document.createElement('div');
        div.setAttribute('page-index', i);
        div.textContent = i;
        div.className = 'item-page';
        if(i === c)
        {
            div.style.backgroundColor = 'red';
            div.style.color = 'white';
        }
        
        div.addEventListener('click', async function(){
            var current2 = parseInt(this.getAttribute('page-index'));
            var items = await get_listed(current2, 'inline');
            addToGrid(items, listedContainer);
            upDate_Nav(current2);
            itemsPageContainer.setAttribute('data-page', current2);

        })
        itemsPageContainer.appendChild(div);
    }

    if(b !== total)
    {
        var div = document.createElement('div');
        div.setAttribute('page-index', i);
        div.textContent = '...';
        div.className = 'item-page';
        itemsPageContainer.appendChild(div);

        var div = document.createElement('div');
        div.setAttribute('page-index', total);
        div.textContent = total;
        div.className = 'item-page';
        
        div.addEventListener('click', async function(){
            var current2 = parseInt(this.getAttribute('page-index'));
            var items = await get_listed(current2, 'inline');
            addToGrid(items, listedContainer);
            upDate_Nav(current2)
            itemsPageContainer.setAttribute('data-page', current2);
        })
        itemsPageContainer.appendChild(div);
    }
}

    

    prevItemsPage.addEventListener('click', async function()
    {
        var current2 = parseInt(itemsPageContainer.getAttribute('data-page'));
        
        
        if(current2 === 1)
        {
            return;
        }
        
        
        var items = await get_listed(current2-1, 'listed_items');
        addToGrid(items, listedContainer);
        itemsPageContainer.setAttribute('data-page', current2-1);
        upDate_Nav(current2-1);
    })

    nextItemsPage.addEventListener('click', async function()
    {

        var current2 = parseInt(itemsPageContainer.getAttribute('data-page'));
        
        if(current2 === total)
        {
            return;
        }
        
        var items = await get_listed(current2+1, 'listed_items');
        addToGrid(items, listedContainer);
        itemsPageContainer.setAttribute('data-page', current2+1);
        upDate_Nav(current2+1);
        
    })

    var items = await get_listed(current, 'inline');
    
    if(items.length === 0)
    {
        listedContainer.innerHTML = '<p class="empty-grid" >No  Videos Found</p>';
        pagenavigatorcontainer.style.display = 'none';

    }
    else{
        listedContainer.innerHTML = '';
        upDate_Nav(current);
        items.forEach(item=>{
            var cus = new NewVideoElement(item);
            listedContainer.append(cus);
        })
    }
    
})