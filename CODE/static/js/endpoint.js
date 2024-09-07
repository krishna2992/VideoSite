async function endpoint_index(page=1)
{
    const response = await fetch(`/endpoint/?page=${page}`);
    if(!response.ok)
    {
        return [];
    }
    return response.json();
}
async function endpoint_recent(page=1)
{
    const response = await fetch(`/endpoint/recent?page=${page}`);
    if(!response.ok)
    {
        return [];
    }
    return response.json();
}

async function endpoint_full(page=1)
{
    const response = await fetch(`/endpoint/full?page=${page}`);
    if(!response.ok)
    {
        return [];
    }
    return response.json();
}

async function endpoint_viewed(page=1)
{
    const response = await fetch(`/endpoint/most/viewed?page=${page}`);
    if(!response.ok)
    {
        return [];
    }
    return response.json();
}

async function endpoint_tag(page=1, uuid)
{
    const response = await fetch(`/endpoint/tag/${uuid}?page=${page}`);
    if(!response.ok)
    {
        return [];
    }
    return response.json();
}

async function endpoint_actor(page=1, uuid)
{
    const response = await fetch(`/endpoint/actor/${uuid}?page=${page}`);
    if(!response.ok)
    {
        return [];
    }
    return response.json();
}

async function endpoint_items(page, type, data)
{
    if(type === 'index')
    {
        return await endpoint_index(page);
    }
    else if(type == 'recent')
    {
        return await endpoint_recent(page);
    }
    else if(type === 'viewed')
    {
        return await endpoint_viewed(page);
    }
    else if(type === 'full')
    {
        return await endpoint_full(page);
    }
    else if(type === 'tag')
    {
        return await endpoint_tag(page, data['uuid']);
    }
    else if(type === 'actor')
    {
        return await endpoint_actor(page, data['uuid']);
    }
    return await endpoint_index(page);
}