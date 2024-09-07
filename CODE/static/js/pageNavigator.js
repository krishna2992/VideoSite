document.addEventListener('DOMContentLoaded', function(){
    
        var itemsPageContainer = document.getElementById('itempageBoxContainer')    
        var current = parseInt(itemsPageContainer.getAttribute('data-page'));
        var total = parseInt(itemsPageContainer.getAttribute('data-length'));
        var start =current- current%5+1;
        var end  = (start+5-1)<total?start+5-1:total;
        var prevItemsPage = document.getElementById('prevItemsPage');
        var nextItemsPage = document.getElementById('nextItemsPage');
        

        for(var i= start; i <= end; i++)
        {
            
            var div = document.createElement('div');
            div.setAttribute('page-index', i);
            div.textContent = i;
            div.className = 'item-page';
            if(i === current)
            {
                div.style.backgroundColor = 'red';
                div.style.color = 'white';
            }
            
            div.addEventListener('click', function(){
                window.location.href = window.location.href.split('?')[0]+`?page=${this.getAttribute('page-index')}`;
            })
            itemsPageContainer.appendChild(div);
        }

        if(end !== total)
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
            
            div.addEventListener('click', function(){
                window.location.href = window.location.href.split('?')[0]+`?page=${this.getAttribute('page-index')}`;
            })
            itemsPageContainer.appendChild(div);
        }

        prevItemsPage.addEventListener('click', function(){
            if(current > 1)
            {
                window.location.href = window.location.href.split('?')[0]+`?page=${current-1}`;
            }
        })

        nextItemsPage.addEventListener('click', function(){
            if(current < total)
            {
                window.location.href = window.location.href.split('?')[0]+`?page=${current+1}`;
            }
        })

})