function add_category(camp_id) {
    // using ajax to send the data to the server
    $.ajax({
        url: "/camp/add_category",
        method: "POST",
        data: {
            "category_name": $("#category_name").val(),
            "category_color": $("#category_color").val(),
            "camp_id": camp_id
        },
        success: function (res) {
            var code = res['code'];
            if (code === 200) {
                window.location.reload();
            } else {
                layer.msg(res['message']);
            }
        }
    })
}

// function for deleting the category
function delete_category(category_id) {
    $.ajax({
        url: "/camp/delete_category",
        method: "POST",
        data: {
            "category_id": category_id
        },
        success: function (res) {
            var code = res['code'];
            if (code === 200) {
                window.location.reload();
            } else {
                layer.msg(res['message']);
            }
        }
    })
}