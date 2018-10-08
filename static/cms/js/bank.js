$(function () {
    $("#saveBank").click(function (ev) {
        var saveoradd = $(this).attr('from');
        if (saveoradd == 1) {
            var url = "/cms/updatebank/";
        } else {
            url = "/cms/addbank/";
        }
        bankname=$("#bankname").val();
        id=$("#id").val();
        csrf = $('meta[name=csrf_token]').attr("value");
        ev.preventDefault();
        $.ajax({
            url: url,
            type: "post",
            data: {
                "bankname": bankname,
                "id": id,
                'csrf_token':csrf,
            },
            success: function (data) {
                if (data.code == 200) {
                    xtalert.alertSuccessToast(data.msg);
                    window.location = "/cms/bank/"
                } else {
                    xtalert.alertErrorToast(data.msg)
                }
            }
        })
    });
    $('.update-btn').click(function () {
        self = $(this);
        $('#myModal').modal('show');// 让模态框出来
        $('meta[name=csrf_token]').attr("value");
        $("#data-bankname").val(self.attr('data-bankname'));
        $('#saveBank').attr("from", '1');
        $('#id').val(self.attr('data-id'));
        console.log($('#id').val())
    });
    $('#myModal').on('hidden.bs.modal', function (e) {
        e.preventDefault();
        $('#saveBank').attr("from", '0')
    });
    $('.delete-btn').click(function (ev) {
        csrf = $('meta[name=csrf_token]').attr("value");
        id=$(this).attr('data-id');
        ev.preventDefault();
        $.ajax({
            url: '/cms/delebank/',
            type: 'post',
            data: {
                'csrf_token': csrf,
                'id': id
            },
            success: function (data) {
                if (data.code == 200) {
                    xtalert.alertSuccessToast("删除成功");
                    window.location.reload(); //  重新加载这个页面
                } else {  // 提示出错误
                    xtalert.alertErrorToast(data.msg)
                }
            }
        })
    });
});