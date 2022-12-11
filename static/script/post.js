var layedit = layui.layedit;
var rich_editor;
layui.use('layedit', function () {
    rich_editor = layedit.build('rich_edit', {
        height: 350,
        tool: ["strong",
            "italic",
            "underline",
            "del",
            "|",
            "left",
            "center",
            "right",
            "image"]
    });
});

function post() {
    // get the title
    var title = document.getElementById("post_title").value;
    // get the category id from the select
    var category_id = document.getElementById("post_category").value;
    // get the rich text editor
    var content = layedit.getContent(rich_editor);
    // get the description
    var description = layedit.getText(rich_editor);
    // check the radio button
    var is_Notice = document.getElementById("Notice").checked;
    var is_Top = document.getElementById("Sticky").checked;
    var camp_id = document.getElementById("post_camp_id").value;
    // using ajax to send the information
    $.ajax({
        url: "/camp/make_post",
        method: "POST",
        data: {
            "title": title,
            "category_id": category_id,
            "content": content,
            "description": description,
            "is_notice": is_Notice,
            "is_top": is_Top
        },
        success: function (res) {
            var code = res['code'];
            if (code === 200) {
                layer.msg("You have successfully posted a new post!");
                // wait for 1 second and reload the page
                setTimeout(function () {
                    window.location.href = "/camp/"+camp_id.toString();
                }, 1000);
            } else {
                layer.msg(res['message']);
            }
        }
    })
}

// using jquery to get the click button
$(function () {
    $("#post_btn").on("click", function (event) {
        post();
    })
})