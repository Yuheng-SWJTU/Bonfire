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