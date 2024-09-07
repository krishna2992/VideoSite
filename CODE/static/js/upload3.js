document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('uploadForm').addEventListener('submit', function(event) {
        event.preventDefault();
        document.getElementById('uploadButton').disabled = true;
        uploadMetadata();
    })  
})
var uploadButton = document.getElementById('uploadButton');
function uploadMetadata() 
{
    let name = document.getElementById('id_name').value;
    let tags = document.getElementById('id_tags').value;
    let actors = document.getElementById('id_actors').value;
    let isFull = document.getElementById('id_isFull');
    let file = document.getElementById('id_video').files[0];
    let profile = document.getElementById('id_profile').files[0];
    
    if (!file) {
        console.error('No file selected.');
        return;
    }   
    console.log(name, tags, actors, isFull, file);
    let formData = new FormData();
    formData.append('name', name);
    formData.append('tags', tags);
    formData.append('actors', actors);
    formData.append('profile', profile);

    if(isFull.checked)
    {
        formData.append('isFull', isFull);
    }

    fetch('/Upload/', {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': getCookie('csrftoken') // Ensure you have a function to get CSRF token
        }
    })
    .then(response => response.json())
    .then(data => {
        var fileId = data.unique_uuid; // Assuming backend returns the unique identifier as 'file_id'
        console.log('Metadata uploaded. File ID:', fileId);
        uploadFile(fileId); 
    })
    .catch(error => console.error('Error uploading metadata:', error));
}

function uploadFile(fileId) 
{
    let file = document.getElementById('id_video').files[0];
    if (!fileId) 
    {
        console.error('File ID is missing. Upload metadata first.');
        return;
    }

    const chunkSize = 5*1024 * 1024;
    const totalChunks = Math.ceil(file.size/chunkSize);
    var failed_chunks = [];
    var  total = 0;

    async function finalize_upload(iteration)
    {
        if(iteration > 0 && failed_chunks.length !== 0)
        {
            const responce = await cancel_upload(fileId);
            alert('Failed to Upload. Plaease Try Again');
            window.location = '/user/home';
            return;
        }
        const failed  = [...failed_chunks];
        if (failed_chunks.length > 0)
        {
            failed_chunks = [];
            uploadChunk(failed, 0,iteration+1);
        }
        else{
            const res = await upload_complete(fileId);
            if(res.status === 201)
            {
                alert('File upload complete');
                window.location ='/user/home';
                return;
            }
            alert('File upload failed');
            window.location ='/user/home';
            return;
        }
    }

    function uploadChunk(failed_list ,i, iteration) 
    {
        if(i>= totalChunks)
        {
            finalize_upload(iteration);
            return;
        }
        var chunk_num = i;
        if(failed_list)
        {
            if(i < failed_list.length)
            {
                chunk_num = failed_list[i];
            }
            else
            {
                finalize_upload(iteration);
                return;
            }
    
        }
        const end = Math.min((chunk_num + 1) * chunkSize, file.size);
        const chunk = file.slice(chunk_num * chunkSize, end);
        
        let formData = new FormData();
        formData.append('file', chunk);
        formData.append('chunk_seq', i);
        formData.append('file_id', fileId);
        formData.append('total', totalChunks);

fetch('/Upload/chunk', {
    method: 'POST',
    body: formData,
    headers: {
        'X-CSRFToken': getCookie('csrftoken') // Ensure CSRF token is included
    }
})
.then(response => {
    if (!response.ok) {
        throw new Error('Upload failed');
    }
    return response.json();
})
.then(result => {
    console.log('Chunk uploaded:', result);
    total += chunkSize;
    const percentComplete = Math.round((total / file.size) * 100);
    document.getElementById('progressBar').value = percentComplete;
    uploadChunk(failed_list, i+1, iteration);
})
.catch(error => {
    console.error('Error uploading chunk:', error);
    failed_chunks.append(i)
    uploadChunk(failed_list, i+1, 0);
});
}
uploadChunk(null , 0, 0);
}
