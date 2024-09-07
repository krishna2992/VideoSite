async function get_unattended()
{
    const responce = await fetch('/api/channel/unlisted');
    if(!responce.ok)
    {
        console.log(responce)
        return []
    }
    const data = await responce.json();
    return data;
}

async function get_listed(page, source)
{
    const responce = await fetch(`/api/channel/listed?page=${page}&source=${source}`);
        if(!responce.ok)
        {
            console.log(responce)
            throw new Error('Network response was not ok');
            return
        }
        const data = await responce.json();
        return data;
}

async function cancel_upload(upload_uuid)
{
    const responce = await fetch(`/api/invalidate/upload/${upload_uuid}`);
    if(!responce.ok)
    {
        console.log(responce)
        throw new Error('Network response was not ok');
    }
    const data = await responce.json();
    return data;
}

async function upload_complete(upload_uuid)
{
    const responce = await fetch(`/api/complete/upload/${upload_uuid}`);
    return responce;
}


async function get_favourites()
{
    const responce = await fetch('/api/favourites');
        if(!responce.ok)
        {
            console.log(responce)
            return [];
        }
        const data = await responce.json();
        return data;
}