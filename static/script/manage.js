layui.use(['upload', 'element', 'layer'], function () {
    var $ = layui.jquery
        , upload = layui.upload
        , element = layui.element
        , layer = layui.layer;

    var uploadInst = upload.render({
        elem: '#re_upload_background'
        , url: '/camp/upload_background'
        , before: function (obj) {
            //预读本地文件示例，不支持ie8
            obj.preview(function (index, file, result) {
                $('#re_upload_background').attr('src', result);
            });

            element.progress('re_upload_back_progress', '0%');
            layer.msg('Uploading...', {icon: 12, time: 0});
        }
        , done: function (res) {
            if (res.code > 0) {
                return layer.msg('Failed');
            }
            $('#demoText').html('');
        }
        , error: function () {
            var demoText = $('#demoText');
            demoText.html('<span style="color: #FF5722;">Failed</span> <a class="layui-btn layui-btn-xs demo-reload">Retry</a>');
            demoText.find('.demo-reload').on('click', function () {
                uploadInst.upload();
            });
        }
        , progress: function (n, elem, e) {
            element.progress('re_upload_back_progress', n + '%');
            if (n == 100) {
                layer.msg('Completed', {icon: 1});
            }
        }
    });
});

function add_admin(camp_id) {
    // using ajax to send the request
    $.ajax({
        url: "/camp/add_admin",
        method: "POST",
        data: {
            "camp_id": camp_id,
            "username": $("#add_admin").val()
        },
        success: function (res) {
            var code = res['code'];
            if (code === 200) {
                layer.msg("Add admin successfully!");
                // wait for 1 second and reload the page
                setTimeout(function () {
                    window.location.reload();
                }, 1000);
            } else {
                layer.msg(res['message']);
            }
        }
    })
}

function delete_admin(camp_id, admin_id, admin_name) {

    layer.confirm('You are going to remove the Admin identity of<br>' + admin_name, {
        title: "Remove Admin",
        btn: ['Remove', 'Cancel'] //按钮
    }, function () {
        $.ajax({
            url: "/camp/remove_admin",
            method: "POST",
            data: {
                "camp_id": camp_id,
                "admin_id": admin_id
            },
            success: function (res) {
                var code = res['code'];
                if (code === 200) {
                    layer.msg("Delete admin successfully!");
                    // wait for 1 second and reload the page
                    setTimeout(function () {
                        window.location.reload();
                    }, 1000);
                } else {
                    layer.msg(res['message']);
                }
            }
        }
    )
    }, function () {
    });
}

function edit_camp(camp_id){
    // using ajax to send the request
    $.ajax({
        url: "/camp/edit_camp",
        method: "POST",
        data: {
            "camp_id": camp_id,
            "camp_name": $("#manage_camp_name").val(),
            "camp_description": $("#manage_camp_description").val()
        },
        success: function (res) {
            var code = res['code'];
            if (code === 200) {
                layer.msg("Edit camp successfully!");
                // wait for 1 second and reload the page
                setTimeout(function () {
                    window.location.reload();
                } , 1000);
            } else {
                layer.msg(res['message']);
            }
        }
    })
}

function dismiss_camp(camp_id) {
    // using ajax to send the request
    layer.confirm('You are going to dismiss the camp<br><br>All resources in the camp will be deleted<br><br>This operation cannot be restored!', {
        title: "WARNING",
        btn: ['Dismiss', 'Cancel'] //按钮
    }, function () {
        $.ajax({
            url: "/camp/dismiss_camp",
            method: "POST",
            data: {
                "camp_id": camp_id
            },
            success: function (res) {
                var code = res['code'];
                if (code === 200) {
                    layer.msg("Delete camp successfully!");
                    // wait for 1 second and reload the page
                    setTimeout(function () {
                        window.location.href = "/";
                    }, 1000);
                } else {
                    layer.msg(res['message']);
                }
            }
        }
    )
    }, function () {
    });
}

function checkEditCampForm() {
    // check the camp name
    jQuery.validator.addMethod("itemPass", function (value, element) {
        var reg = /^\w+$/;
        return this.optional(element) || (reg.test(value));
    })

    jQuery.validator.addMethod("itemName", function (value, element) {
        var reg = /^[A-Za-z]+$/;
        return this.optional(element) || (reg.test(value));
    })

    $("#edit-camp").validate({
        rules: {
            manage_camp_name: {
                required: true,
                itemPass: true,
                minlength: 3,
                maxLength: 20
            },
            manage_camp_description: {
                required: true,
                itemPass: true,
                minlength: 3,
                maxLength: 100
            }
        },
        messages: {
            manage_camp_name: {
                required: "Please enter the camp name",
                itemPass: "Only letters and numbers are allowed",
                minlength: "The camp name should be at least 3 characters",
                maxLength: "The camp name should be at most 20 characters"
            },
            manage_camp_description: {
                required: "Please enter the camp description",
                itemPass: "Only letters and numbers are allowed",
                minlength: "The camp description should be at least 3 characters",
                maxLength: "The camp description should be at most 100 characters"
            }
        }
    })
}

// wait for the web page to load all elements
$(function () {
        checkEditCampForm();
    }
)