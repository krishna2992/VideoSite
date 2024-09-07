var notification = document.getElementById('notification');
function checkNotification() 
{
    if (!getCookie('notificationShown'))
    {
        notification.style.display = 'flex';
    }
    
}
document.addEventListener('DOMContentLoaded', checkNotification);
    var warningButton = document.getElementById('warningButton');
    warningButton.addEventListener('click', function(){
        notification.style.display = 'none';
        setCookie('notificationShown', true, 30)
})