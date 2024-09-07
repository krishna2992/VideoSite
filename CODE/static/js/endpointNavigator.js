document.addEventListener('DOMContentLoaded', async function(){
    var gridContainer = document.getElementById('gridContainer');
    var itemsPageContainer = document.getElementById('itempageBoxContainer')    
    var current = parseInt(itemsPageContainer.getAttribute('data-page'));
    var total = parseInt(itemsPageContainer.getAttribute('data-length'));
    var start =current- current%5+1;
    var prevItemsPage = document.getElementById('prevItemsPage');
    var nextItemsPage = document.getElementById('nextItemsPage');
    var type = itemsPageContainer.getAttribute('data-type');
    var data = {
        'uuid' :gridContainer.getAttribute('data-id'),
    };


    

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
            var items = await endpoint_items(current2, type, data);
            addToGrid(items, gridContainer);
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
            var items = await endpoint_items(current2, type, data);
            addToGrid(items, gridContainer);
            upDate_Nav(current2)
            itemsPageContainer.setAttribute('data-page', current2);
        })
        itemsPageContainer.appendChild(div);
    }
}

    

    prevItemsPage.addEventListener('click', async function(){
        var current2 = parseInt(itemsPageContainer.getAttribute('data-page'));
        if(current2 > 1)
        {
            
            var items = await endpoint_items(current2-1, type, data);
            addToGrid(items, gridContainer);
            upDate_Nav(current2-1);
            itemsPageContainer.setAttribute('data-page', current2-1);
        }
    })

    nextItemsPage.addEventListener('click', async function(){
        var current2 = parseInt(itemsPageContainer.getAttribute('data-page'));
        if(current2 < total)
        {
            
            var items = await endpoint_items(current2+1, type, data);
            addToGrid(items, gridContainer);
            upDate_Nav(current2+1);
            itemsPageContainer.setAttribute('data-page', current2+1);
        }
    })

    if(total !== 0)
    {
        var initial = await endpoint_items(current, type, data);
        addToGrid(initial, gridContainer);
        upDate_Nav(current);
    }
    else{

        prevItemsPage.style.display = 'none';
        nextItemsPage.style.display = 'none';
        gridContainer.innerText = 'No Videos Available';
    
    }

})