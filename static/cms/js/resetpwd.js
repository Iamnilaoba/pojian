$(function () {
    $('#resetpwdbtn').click(function (ev) {
        ev.preventDefault();
        oldpwd=$('#oldpwd').val();
        newpwd=$('#newpwd').val();
        newpwd2=$('#newpwd2').val();
        csrf=$('meta[name=csrf_token]').attr('value');
        $.ajax({
            url:'/cms/resetpwd/',
            type:'post',
            data:{
                'oldpwd':oldpwd,
                'newpwd':newpwd,
                'newpwd2':newpwd2,
                'csrf_token':csrf,
            },
            success:function (data) {
                if(data.code==200){
                    xtalert.alertSuccessToast('修改密码成功');
                    $('#oldpwd').val('');
                    $('#newpwd').val('');
                    $('#newpwd2').val('')
                }else {
                    xtalert.alertErrorToast(data.msg);
                }
            }
        })
    })
});







