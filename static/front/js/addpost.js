
$(function () {
    //富文本
     var ue = UE.getEditor("editor",{
         'serverUrl': '/upload/'
     });

     $('#addpost').click(function (ev) {
         ev.preventDefault();
         var title = $('input[name=postname]');
         var bank_id = $('select[name=boarderid]');
         var content = ue.getContent();
        $.ajax({
            url:'/addpost/',
            type:'post',
            data:{
                'title':title.val(),
                'bank_id':bank_id.val(),
                "csrf_token":$("#csrf_token").attr("value"),
                'content':content
            },
            success:function (data) {
                if (data.code == 200) {
                     xtalert.alertSuccessToast("发帖成功");
                    window.location.href = '/'
                } else {
                    console.log(data.msg);
                }
            }
        })
     })
})

