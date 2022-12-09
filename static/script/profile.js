//prompt层
function edit_name() {
    layer.prompt({title: 'Edit your username', formType: 0, btn:['Confirm']}, function (text, index) {
        layer.close(index);
        $.ajax({
            url: "/user/edit_name",
            method: "POST",
            data: {
                "new_name": text
            },
            success: function (res) {
                var code = res['code']
                if (code === 200) {
                    // refresh the page
                    window.location.reload();
                } else {
                    layer.msg(res['message']);
                }
            },
            }
        )
    });
}

//prompt层
function edit_description() {
    layer.prompt({title: 'Edit your description', formType: 2, btn:['Confirm']}, function (text, index) {
        layer.close(index);
        $.ajax({
            url: "/user/edit_description",
            method: "POST",
            data: {
                "new_description": text
            },
            success: function (res) {
                var code = res['code']
                if (code === 200) {
                    // refresh the page
                    window.location.reload();
                } else {
                    layer.msg(res['message']);
                }
            },
            }
        )
    });
}

layui.use(['upload', 'element', 'layer'], function() {
    var $ = layui.jquery
        , upload = layui.upload
        , element = layui.element
        , layer = layui.layer;

    //常规使用 - 普通图片上传
    var uploadInst = upload.render({
        elem: '#avatar'
        , url: '/user/upload_avatar' //此处用的是第三方的 http 请求演示，实际使用时改成您自己的上传接口即可。
        , before: function (obj) {
            //预读本地文件示例，不支持ie8
            obj.preview(function (index, file, result) {
                $('#avatar').attr('src', result); //图片链接（base64）
            });
            layer.msg('Uploading...', {icon: 12, time: 0});
        }
        , done: function (res) {
            //如果上传失败
            if (res.code > 0) {
                return layer.msg(res['message']);
            }
            //上传成功
            // refresh the page
            window.location.reload();
            $('#demoText').html(''); //置空上传失败的状态
        }
        , error: function () {
            //演示失败状态，并实现重传
            var demoText = $('#demoText');
            demoText.html('<span style="color: #FF5722;">Failed</span> <a class="layui-btn layui-btn-xs demo-reload">Retry</a>');
            demoText.find('.demo-reload').on('click', function () {
                uploadInst.upload();
            });
        }
        //进度条
        , progress: function (n, elem, e) {
            if (n === 100) {
                layer.msg('Completed', {icon: 1});
            }
        }
    });
});

function bindCaptchaBtnClick() {
    $("#captcha-btn").on("click", function (event) {
        var $this = $(this)
        // Send the request throw js：ajax：Async Javascript And XML
        $.ajax({
            url: "/user/get_change_password_captcha",
            method: "POST",
            success: function (res) {
                var code = res['code']
                if (code === 200) {
                    // cancel the click event
                    $this.off("click")
                    // start the countdown
                    var countDown = 60;
                    var timer = setInterval(function () {
                        if (countDown > 0) {
                            $this.text(countDown + " s")
                        } else {
                            $this.text("Send");
                            // rebind the click event
                            bindCaptchaBtnClick();
                            // If the countdown is not needed, it needs to be cleared,
                            // otherwise it will continue to execute
                            clearInterval(timer)
                        }
                        countDown -= 1;
                    }, 1000)
                    layer.msg("Captcha has been sent to your e-mail!")
                } else {
                    layer.msg(res['message']);
                }
            }
        })
    })
}


function checkChangePasswordForm(){
    jQuery.validator.addMethod("itemPass", function (value, element) {
        var reg = /^\w+$/;
        return this.optional(element) || (reg.test(value));
    })

    jQuery.validator.addMethod("itemName", function (value, element) {
        var reg = /^[A-Za-z]+$/;
        return this.optional(element) || (reg.test(value));
    })

    $("#change_pswd").validate({
        rules: {
            password: {
                required: true,
                itemPass:true,
                minlength: 6,
                maxLength: 40
            },
            captcha: {
                required: false,
            },
            password_con:{
                required: true,
                equalTo: "#password"
            }
        },
        messages: {
            password: {
                required: "Please enter your password",
                itemPass: "The password can only be composed of letters, numbers and underscores",
                minlength: "The password is between 6 and 40 characters"
            },
            captcha: {
                required: "Please enter the verification code",
            },
            password_con:{
                required: "Please enter your password again",
                equalTo: "The two passwords are inconsistent"
            }
        }
    })
}

function confirm_pswd() {
    $.ajax({
        url: "/user/edit_password",
        method: "POST",
        data: {
            "password": $("#password").val(),
            "captcha": $("#captcha").val(),
            "password_con": $("#password_con").val()
        },
        success: function (res) {
            var code = res['code']
            if (code === 200) {
                layer.msg(res['message']);
            } else {
                layer.msg(res['message']);
            }
        }
    })
}

// wait for the web page to load all elements
$(function () {
        bindCaptchaBtnClick();
        checkChangePasswordForm();
    }
)