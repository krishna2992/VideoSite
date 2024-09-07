// document.getElementById('likeButton').addEventListener('click', function() {
//     const postId = this.dataset.postId;
//     this.classList.add('enlarged');
    
//     fetch(`/like/${postId}/`, {
//         method: 'POST',
//         headers: {
//             'X-CSRFToken': '{{ csrf_token }}',
//             'Content-Type': 'application/json',
//         },
//         credentials: 'same-origin',
//     })
//     .then(response => response.json())
//     .then(data => {
//         if (data.liked) {
//             this.textContent = 'Liked';
//         } else {
//             this.textContent = 'Like';
//         }
//         // You can update the like count here if you want
//     })
//     .catch(error => console.error('Error:', error));
//     this.classList.remove('enlarged');
// });


document.getElementById('shareButton').addEventListener('click', function() {
    const mainUrl = window.location.href;

    // Create a temporary input element
    const tempInput = document.createElement('input');
    tempInput.value = mainUrl;
    document.body.appendChild(tempInput);

    // Select the input field
    tempInput.select();
    tempInput.setSelectionRange(0, 99999); // For mobile devices

    // Copy the text inside the input field
    document.execCommand('copy');
    
    // Remove the input element
    document.body.removeChild(tempInput);

    // Inform the user
    alert('URL copied to clipboard: ' + mainUrl);
});


