toastr.options = {
    "closeButton": true,
    "debug": false,
    "progressBar": false,
    "positionClass": "toast-top-full-width",
    "onclick": null,
    "showDuration": "1600",
    "hideDuration": "1000",
    "timeOut": "5000",
    "extendedTimeOut": "1000",
    "showEasing": "swing",
    "hideEasing": "linear",
    "showMethod": "fadeIn",
    "hideMethod": "fadeOut"
};

$(function(){
    $( "#LoginForm" ).submit(function( event ) {
        toastr.clear();
        var img = $('<img />', {
          id: 'loader',
          src: '/static/img/custom/loader.gif',
          alt: 'Loader',
          style: ""
        });
        img.appendTo($("#LoginSubmitButton"));

        var action = $(this).attr("action");
        var data = $(this).serializeArray();
            $.ajax(
            {
                url : action,
                type: "POST",
                data : data,
                success:function(data, textStatus, jqXHR)
                {
                    if(data.status == 1){
                        toastr.success(data.message);
                    }else var msg;
                    if (data.status == 0) {
                        msg = "Giriş yapılırken hata oluştu. Lütfen hataları düzelttikten sonra tekrar deneyiniz<br/>";
                        $.each($.parseJSON(data.errors), function (k, v) {
                            msg += (v[0].message + "<br/>");
                        });
                        toastr.error(msg);
                    }

                },
                error: function(jqXHR, textStatus, errorThrown)
                {
                    //if fails
                }
            }).done(function() {
                    $("#loader").remove();
                });
        event.preventDefault();
    });
});