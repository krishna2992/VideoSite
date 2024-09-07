window.onload = function(){
    document.getElementById('id_tags').value = '';
    document.getElementById('id_actors').value = '';
}

var actorSelect = document.getElementById('id_actors_select');
var actors = document.getElementById('id_actors');
var actorFilter = document.getElementById('id_filter_actors');
var selectedActors = document.getElementById('selectedActors');
var createActorButton = document.getElementById('actorCreateButton');



actorFilter.addEventListener('input', function(){
    var filterValue = this.value.toLowerCase();
    if(!filterValue || filterValue == '')
    {
        createActorButton.textContent = ``;
        createActorButton.value = '';
        createActorButton.style.display = 'none';   
    }
    var options = actorSelect.querySelectorAll('option');
    var count = 0;
    options.forEach(function(option) 
    {
        var text = option.textContent.toLowerCase();
        if (text.indexOf(filterValue) > -1) 
        {
            option.style.display = '';
            count+=1;
        } 
        else 
        {
            option.style.display = 'none';
        }
    });

    if(count === 0)
    {
        const parts = this.value.split(' ');
        for(var i=0; i< parts.length; i++)
        {
            parts[i] = parts[i].charAt(0).toUpperCase()+parts[i].slice(1);
        }
        var res = parts.join(" ");;
        createActorButton.textContent = `Create '${res}'`;
        createActorButton.value = res;
        createActorButton.style.display = 'block';   
    }
    else{
        createActorButton.textContent = '';
        createActorButton.value = '';
        createActorButton.style.display = 'none';   
    }

})

createActorButton.addEventListener('click', function(event){
    event.preventDefault();
    var val = this.textContent;
    if(!val || val === '')
    {
        return;
    }
    createActorButton.style.display = 'none';
    var option = document.createElement('p');
    option.value = this.value;
    actors.value += ','+this.value;
    actorFilter.value = '';
    
    
    var vals = actors.value.split(',');
    selectedActors.innerHTML = ' ';
    vals.forEach(val=>{
        if(val){
            var p = document.createElement('p');
            p.className = 'selected';
            p.textContent = val;
            selectedActors.appendChild(p);
        }
    })
})

actorSelect.addEventListener('change', function(){
    var selectedActorOption = actorSelect.options[actorSelect.selectedIndex];
    actorFilter.value = ' ';
    if(selectedActorOption.value)
    {
        actors.value += ','+selectedActorOption.value;
        var vals = actors.value.split(',');
        selectedActors.innerHTML = '';
        selectedActorOption.remove()
        vals.forEach(val=>{
            if(val){
                var p = document.createElement('p');
                p.className = 'selected';
                p.textContent = val;
                selectedActors.appendChild(p);
            }
        })
    }
})

var tagSelect = document.getElementById('id_tags_select');
var tags = document.getElementById('id_tags');
var tagFilter = document.getElementById('id_filter_tags');
var selectedTags = document.getElementById('selectedTags');
var createTagButton = document.getElementById('tagCreateButton');



tagFilter.addEventListener('input', function(){
    var filterValue = this.value.toLowerCase();
    if(!filterValue || filterValue == '')
    {
        createTagButton.textContent = `'`;
        createTagButton.value = '';
        createTagButton.style.display = 'none';   
    }
    var options = tagSelect.querySelectorAll('option');
    var count = 0;
    createTagButton.textContent = '';
    createTagButton.style.display = 'none';
    options.forEach(function(option) 
    {
        var text = option.textContent.toLowerCase();
        if (text.indexOf(filterValue) > -1) 
        {
            option.style.display = '';
            count+=1;
        } 
        else 
        {
            option.style.display = 'none';
        }
    });
    if(count === 0)
    {
        const parts = this.value.split(' ');
        for(var i=0; i< parts.length; i++)
        {
            parts[i] = parts[i].charAt(0).toUpperCase()+parts[i].slice(1);
        }
        var res = parts.join(" ");;
        createTagButton.textContent = `Create '${res}'`;
        createTagButton.value = res;
        createTagButton.style.display = 'block';
    }
    else{
        createTagButton.textContent = '';
        createTagButton.value = '';
        createTagButton.style.display = 'none';
    }
    
})

createTagButton.addEventListener('click', function(event){
    event.preventDefault();
    var val = this.textContent;
    if(!val || val === '')
    {
        return;
    }
    
    createTagButton.style.display = 'none';
    var option = document.createElement('p');
    option.value = this.value;
    tags.value += ','+this.value;
    alert(tagFilter.value)
    tagFilter.value = '';
    alert(tagFilter.value);
    const event2 = new Event('input', {
        bubbles:true,
        cancelable:true,
    });
    tagFilter.dispatchEvent(event2);
    var vals = tags.value.split(',');
    selectedTags.innerHTML = '';
    vals.forEach(val=>{
        if(val){
            var p = document.createElement('p');
            p.className = 'selected';
            p.textContent = val;
            selectedTags.appendChild(p);
        }
    })
    createTagButton.textContent = '';
    createTagButton.value = '';
    createTagButton.style.display = 'none';
    
})

tagSelect.addEventListener('change', function(){
    var selectedTagOption = tagSelect.options[tagSelect.selectedIndex];
    createTagButton.textContent = '';
    createTagButton.style.display = 'none';
    tagFilter.value = '';
    if(selectedTagOption.value)
    {
        tags.value += ','+ selectedTagOption.value;
        var vals = tags.value.split(',');
        selectedTags.innerHTML = '';
        selectedTagOption.remove()
        vals.forEach(val=>{
            if(val){
                var p = document.createElement('p');
                p.className = 'selected';
                p.textContent = val;
                selectedTags.appendChild(p);
            }
        })

    }
})
