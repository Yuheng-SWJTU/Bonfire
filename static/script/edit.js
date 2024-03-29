let editor;

window.onload = function () {

    var E = window.wangEditor;
    var i18nChangeLanguage = E.i18nChangeLanguage;
    // change language
    i18nChangeLanguage('en');

    const {createEditor, createToolbar} = window.wangEditor

    const editorConfig = {
        placeholder: 'Type here...',
        onChange(editor) {
            const html = editor.getHtml()
            console.log('editor content', html)
            // 也可以同步到 <textarea>
        },
        MENU_CONF: {}
    }

    editorConfig.MENU_CONF['uploadImage'] = {
        server: '/camp/upload_image',
        timeout: 30 * 1000,
        // 单个文件的最大体积限制，默认为 2M
        maxFileSize: 2 * 1024 * 1024, // 1M

        // 最多可上传几个文件，默认为 100
        maxNumberOfFiles: 4,

        onSuccess(file, res) {
            layer.msg("Image uploaded successfully!");
        },
    }

    // get content from id="edit_content"
    var content = document.getElementById("edit_content").value;
    console.log(content);

    editor = createEditor({
        selector: '#editor-container-edit',
        html: content,
        config: editorConfig,
        mode: 'simple', // or 'simple'
    })

    const toolbarConfig = {}

    const toolbar = createToolbar({
        editor,
        selector: '#toolbar-container-edit',
        config: toolbarConfig,
        mode: 'simple', // or 'simple'
    })
}

function edit() {
    // get the title
    var title = document.getElementById("post_title").value;
    // get the category id from the select
    var category_id = document.getElementById("post_category").value;
    // get the rich text editor
    var content = editor.getHtml();
    // get the description
    var description = editor.getText();
    // check the radio button
    var is_Notice = document.getElementById("Notice").checked;
    var is_Top = document.getElementById("Sticky").checked;
    var camp_id = document.getElementById("post_camp_id").value;
    var edit_id = document.getElementById("edit_id").value;
    // using ajax to send the information
    $.ajax({
        url: "/camp/edit_post",
        method: "POST",
        data: {
            "title": title,
            "category_id": category_id,
            "content": content,
            "description": description,
            "is_notice": is_Notice,
            "is_top": is_Top,
            "post_id": edit_id,
        },
        success: function (res) {
            var code = res['code'];
            if (code === 200) {
                layer.msg("You have successfully edit this post!");
                // wait for 1 second and reload the page
                setTimeout(function () {
                    window.location.href = "/camp/" + camp_id.toString();
                }, 1000);
            } else {
                layer.msg(res['message']);
            }
        }
    })
}

function leave_camp() {
    // using ajax to send the request

    layer.confirm('You are leaving this camp!<br>This operation cannot be restored!', {
        title: "WARNING",
        btn: ['Leave', 'Cancel'] //按钮
    }, function () {
        $.ajax({
                url: "/camp/leave_camp",
                method: "POST",
                success: function (res) {
                    var code = res['code']
                    if (code === 200) {
                        layer.msg(res['message']);
                        // redirect to the index page
                        window.location.href = "/";
                    } else {
                        layer.msg(res['message']);
                    }
                }
            }
        )
    }, function () {
    });
}

// using jquery to get the click button
$(function () {
    $("#edit_btn").on("click", function (event) {
        edit();
    })
    $("#leave-camp").on("click", function (event) {
        leave_camp();
    })
})