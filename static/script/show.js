function favorite(post_id){
    $.ajax({
        url: "/camp/favorite",
        method: "POST",
        data: {
            "post_id": post_id,
        },
        success: function (res) {
            var code = res['code'];
            if (code === 200) {
                layer.msg(res['message']);
                if (res["status"] === "success"){
                    // change the color of the favorite button
                    $("#favorite").css("background-color", "#886be4");
                }
                if (res["status"] === "cancel"){
                    // change the color of the favorite button
                    $("#favorite").css("background-color", "#b5a6ec");
                }
            } else {
                layer.msg(res['message']);
            }
        }
    })
}

function like(post_id){
    $.ajax({
        url: "/camp/like",
        method: "POST",
        data: {
            "post_id": post_id,
        },
        success: function (res) {
            var code = res['code'];
            if (code === 200) {
                layer.msg(res['message']);
                if (res["status"] === "success"){
                    // change the color of the like button
                    $("#like").css("background-color", "#886be4");
                }
                if (res["status"] === "cancel"){
                    // change the color of the like button
                    $("#like").css("background-color", "#b5a6ec");
                }
                // change the number of likes
                $("#like-count").text(res["like_count"]);
            } else {
                layer.msg(res['message']);
            }
        }
    })
}

function delete_post(post_id, camp_id){
    $.ajax({
        url: "/camp/delete_post",
        method: "POST",
        data: {
            "post_id": post_id,
        },
        success: function (res) {
            var code = res['code'];
            if (code === 200) {
                layer.msg(res['message']);
                // wait for 1 second and then jump to the camp page
                setTimeout(function () {
                    window.location.href = "/camp/" + camp_id;
                } , 1000);
            } else {
                layer.msg(res['message']);
            }
        }
    })
}

function comment(post_id){
    var content = $("#comment_input").val();
    $.ajax({
        url: "/camp/comment",
        method: "POST",
        data: {
            "post_id": post_id,
            "content": content
        },
        success: function (res) {
            var code = res['code'];
            if (code === 200) {
                layer.msg(res['message']);
                // wait for 1 second and then jump to the camp page
                setTimeout(function () {
                    window.location.reload();
                } , 1000);
            } else {
                layer.msg(res['message']);
            }
        }
    })
}

function delete_comment(comment_id){
    $.ajax({
        url: "/camp/delete_comment",
        method: "POST",
        data: {
            "comment_id": comment_id,
        },
        success: function (res) {
            var code = res['code'];
            if (code === 200) {
                layer.msg(res['message']);
                // wait for 1 second and then jump to the camp page
                setTimeout(function () {
                    window.location.reload();
                } , 1000);
            } else {
                layer.msg(res['message']);
            }
        }
    })
}

function edit_post(post_id, camp_id){
    // access the url
    window.location.href = "/camp/" + camp_id.toString() + "/" + post_id.toString() + "/edit";
}
