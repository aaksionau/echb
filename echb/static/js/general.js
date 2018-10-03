$(document).ready(function(){
    $('#top-menu').on('click', function(){
        $('.main-nav').toggleClass('mobile');
        $('#top-menu i').toggleClass('fa-times');
        return false;
    });
});
function AddSubscriber(){
    $('#subscriberForm').get(0).submit();
}