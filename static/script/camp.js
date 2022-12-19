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

function popularity() {
    // using ajax to send the request
    $.ajax({
            url: "/camp/change_sort",
            method: "POST",
            data: {
                "sort": "popularity"
            },
            success: function (res) {
                var code = res['code']
                if (code === 200) {
                    layer.msg(res['message']);
                    // refresh the page
                    window.location.reload();
                } else {
                    layer.msg(res['message']);
                }
            }
        }
    )
}

function postdate(){
    // using ajax to send the request
    $.ajax({
            url: "/camp/change_sort",
            method: "POST",
            data: {
                "sort": "postdate"
            },
            success: function (res) {
                var code = res['code']
                if (code === 200) {
                    layer.msg(res['message']);
                    // refresh the page
                    window.location.reload();
                } else {
                    layer.msg(res['message']);
                }
            }
        }
    )
}