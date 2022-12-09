function join_camp(camp_id){
    // using ajax to send the request
    $.ajax({
        url: "/join_camp",
        method: "POST",
        data: {
            "camp_id": camp_id
        },
        success: function (res) {
            var code = res['code']
            if (code === 200) {
                layer.msg(res['message']);
                // change the dom '#users_num' to the new number of users
                $('#users_num_'+camp_id).text(res['users_num']);
            } else {
                layer.msg(res['message']);
            }
        }
    })
}