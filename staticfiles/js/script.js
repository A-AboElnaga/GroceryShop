$(document).ready(function() {
    function getCookie(name){
        var cookieValue = null;
        if(document.cookie && document.cookie !== ''){
            var cookies = document.cookie.split(';');
            for(var i = 0; i < cookies.length; i++){
                var cookie = cookies[i].trim();
                if(cookie.substring(0,name.length+1) === (name+'=')){
                    cookieValue = decodeURIComponent(cookie.substring(name.length+1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');
    function csrfSafeMethod(method){
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    $.ajaxSetup({
        beforeSend: function(xhr, settings){
            if(!csrfSafeMethod(settings.type)&& !this.crossDomain){
                xhr.setRequestHeader("X-CSRFToken",csrftoken);
            }
        }
    });
    let $deleteButton = $('#delete-button');
    $('body').on('click', '.delete-modal', function () {
        $deleteButton.attr('href', $(this).attr('data-delete-url'))
    });
    $deleteButton.click(function(e) {
        e.preventDefault(); 
        let $this = $(this);
        
        $.ajax({
            url: $this.attr('href'),
            data: '', 
            method: 'POST',
            success:function () {
                $('#exampleModal').modal('hide');
                $('.delete-modal[data-delete-url="'+$this.attr('href')+'"]').parent().remove()
            } 
        }) 
    });
});