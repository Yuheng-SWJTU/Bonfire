layui.use(['upload', 'element', 'layer'], function() {
    var $ = layui.jquery
        , upload = layui.upload
        , element = layui.element
        , layer = layui.layer;

    //常规使用 - 普通图片上传
    var uploadInst = upload.render({
        elem: '#test1'
        , url: 'https://httpbin.org/post' //此处用的是第三方的 http 请求演示，实际使用时改成您自己的上传接口即可。
        , before: function (obj) {
            //预读本地文件示例，不支持ie8
            obj.preview(function (index, file, result) {
                $('#demo1').attr('src', result); //图片链接（base64）
            });

            element.progress('demo', '0%'); //进度条复位
            layer.msg('Uploading...', {icon: 12, time: 0});
        }
        , done: function (res) {
            //如果上传失败
            if (res.code > 0) {
                return layer.msg('Failed');
            }
            //上传成功的一些操作
            //……
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
            element.progress('demo', n + '%'); //可配合 layui 进度条元素使用
            if (n == 100) {
                layer.msg('Completed', {icon: 1});
            }
        }
    });
});

function checkBuildCampForm(){
    jQuery.validator.addMethod("itemPass", function (value, element) {
        var reg = /^\w+$/;
        return this.optional(element) || (reg.test(value));
    })

    jQuery.validator.addMethod("itemName", function (value, element) {
        var reg = /^[A-Za-z]+$/;
        return this.optional(element) || (reg.test(value));
    })

    $("#build_camp").validate({
        rules: {
            camp_name: {
                required: true,
                minlength: 3,
                maxLength: 20,
                itemName: true
            },
            description: {
                required: true,
                minlength: 3,
                maxLength: 100,
            }
        },
        messages: {
            camp_name: {
                required: "Please enter your camp name",
                minlength: "The camp name is between 4 and 20 characters",
                itemName: "The camp name can only be composed of letters"
            },
            description: {
                required: "Please enter your camp description",
                minlength: "The description is between 4 and 100 characters"
            }
        }
    })
}

// wait for the web page to load all elements
$(function () {
        checkBuildCampForm();
    }
)