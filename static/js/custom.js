toastr.options = {
    "closeButton": true,
    "debug": false,
    "progressBar": false,
    "positionClass": "toast-top-full-width",
    "onclick": null,
    "showDuration": "1600",
    "hideDuration": "1000",
    "timeOut": "10000",
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
        img.appendTo($("#Loading"));

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
                        window.setTimeout(function() {
                                location.href = "/";
                        }, 2000);
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
                    toastr.alert("There was a problem. Please try again.")
                }
            }).done(function() {
                    grecaptcha.reset();
                    $("#loader").remove();
                });
        event.preventDefault();
    });

    $( "#SignUpForm" ).submit(function( event ) {
        toastr.clear();
        var img = $('<img />', {
          id: 'loader',
          src: '/static/img/custom/loader.gif',
          alt: 'Loader',
          style: ""
        });
        img.appendTo($("#Loading"));

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
                        window.setTimeout(function() {
                                location.href = "/giris/";
                        }, 2000);
                    }else var msg;
                    if (data.status == 0) {
                        msg = "Giriş yapılırken hata oluştu. Lütfen hataları düzelttikten sonra tekrar deneyiniz<br/>";
                        $.each($.parseJSON(data.errors), function (k, v) {
                            switch (k){
                                case "username":k="Kullanıcı adı : ";break;
                                case "password1":k="Şifre : ";break;
                                case "password2":k="Şifre tekrar : ";break;
                                case "email":k="Email : ";break;
                                case "first_name":k="İsim : ";break;
                                case "last_name":k="Soyisim : ";break;
                                case "university":k="Üniversite : ";break;
                                case "department":k="Bölüm : ";break;
                                case "grade":k="Sınıf : ";break;
                                case "city":k="Şehir : ";break;
                                case "captcha":k="Captcha : ";break;
                                case "sex":k="Cinsiyet : ";break;
                            }
                            msg += (k + v[0].message + "<br/>");
                        });
                        toastr.error(msg);
                    }

                },
                error: function(jqXHR, textStatus, errorThrown)
                {
                    toastr.alert("There was a problem. Please try again.")
                }
            }).done(function() {
                    grecaptcha.reset();
                    $("#loader").remove();
                });
        event.preventDefault();
    });



    var options = {
        success: showResponse
    };
    $('#ProfileEditForm').submit(function() {
        var img = $('<img />', {
          id: 'loader',
          src: '/static/img/custom/loader.gif',
          alt: 'Loader',
          style: ""
        });
        img.appendTo($("#Loading"));

        $(this).ajaxSubmit(options);
        return false;
    });
    function showResponse(data, statusText, xhr, $form)  {
                    grecaptcha.reset();
                    $("#loader").remove();
                    if(data.status == 1){
                        toastr.success(data.message);
                    }else var msg;
                    if (data.status == 0) {
                        msg = "Güncelleme yapılırken hata oluştu. Lütfen hataları düzelttikten sonra tekrar deneyiniz<br/>";
                        $.each($.parseJSON(data.errors), function (k, v) {
                            switch (k){
                                case "username":k="Kullanıcı adı : ";break;
                                case "password1":k="Şifre : ";break;
                                case "password2":k="Şifre tekrar : ";break;
                                case "email":k="Email : ";break;
                                case "first_name":k="İsim : ";break;
                                case "last_name":k="Soyisim : ";break;
                                case "university":k="Üniversite : ";break;
                                case "department":k="Bölüm : ";break;
                                case "grade":k="Sınıf : ";break;
                                case "city":k="Şehir : ";break;
                                case "captcha":k="Captcha : ";break;
                                case "sex":k="Cinsiyet : ";break;
                            }
                            msg += (k + v[0].message + "<br/>");
                        });
                        toastr.error(msg);
                    }
    }



    var options = {
        success: showThesisResponse
    };
    $('#ThesisCreateForm').submit(function() {
        var img = $('<img />', {
          id: 'loader',
          src: '/static/img/custom/loader.gif',
          alt: 'Loader',
          style: ""
        });
        img.appendTo($("#Loading"));


        $(this).ajaxSubmit(options);
        return false;
    });
    function showThesisResponse(data, statusText, xhr, $form)  {
                    grecaptcha.reset();
                    $("#loader").remove();
                    if(data.status == 1){
                        toastr.success(data.message);
                         window.setTimeout(function() {
                                location.href = "/profil/";
                        }, 2000);
                    }else var msg;
                    if (data.status == 0) {
                        msg = "Güncelleme yapılırken hata oluştu. Lütfen hataları düzelttikten sonra tekrar deneyiniz<br/>";
                        $.each($.parseJSON(data.errors), function (k, v) {
                            switch (k){
                                case "name":k="Başlık : ";break;
                                case "content":k="Açıklama : ";break;
                                case "files":k="Dosya : ";break;
                                case "images":k="Resim : ";break;
                                case "captcha":k="Captcha : ";break;
                            }
                            msg += (k + v[0].message + "<br/>");
                        });
                        toastr.error(msg);
                    }
    }
});