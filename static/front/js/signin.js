$(function () {
    $('#signin_btn').click(function (ev) {
        telephone=$('input[name=telephone]').val();
        csrf=$('meta[name=csrf_token]').attr('value');
        password=$('input[name=password]').val();
        ev.preventDefault();
        $.ajax({
            url:'/signin/',
            type:'post',
            data:{
                'telephone':telephone,
                'csrf_token':csrf,
                'password':password
            },
            success:function (data) {
                if(data.code==200){
                    xtalert.alertSuccessToast('登陆成功');
                    window.location.href='/'
                }else {
                    xtalert.alertErrorToast(data.msg)
                }
            }
        })
    })
});




