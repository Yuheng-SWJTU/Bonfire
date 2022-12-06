layui.use(['upload', 'element', 'layer'], function() {
    var $ = layui.jquery
        , upload = layui.upload
        , element = layui.element
        , layer = layui.layer;

    //常规使用 - 普通图片上传
    var uploadInst = upload.render({
        elem: '#re_upload_background'
        , url: 'https://httpbin.org/post' //此处用的是第三方的 http 请求演示，实际使用时改成您自己的上传接口即可。
        , before: function (obj) {
            //预读本地文件示例，不支持ie8
            obj.preview(function (index, file, result) {
                $('#re_upload_background').attr('src', result); //图片链接（base64）
            });

            element.progress('re_upload_back_progress', '0%'); //进度条复位
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
            element.progress('re_upload_back_progress', n + '%'); //可配合 layui 进度条元素使用
            if (n == 100) {
                layer.msg('Completed', {icon: 1});
            }
        }
    });
});