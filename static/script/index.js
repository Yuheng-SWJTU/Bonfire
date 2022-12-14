function join_camp(camp_id) {
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
                $('#users_num_' + camp_id).text(res['users_num']);
                // wait 1 second and redirect to the camp page
                setTimeout(function () {
                    window.location.href = "/camp/" + res["camp_id"];
                }, 1000);
            } else {
                layer.msg(res['message']);
            }
        }
    })
}

window.onload = function () {
    // if localStorage has the key 'cookie'
    if (localStorage.getItem('cookie')) {
        // hide the cookie alert with a fade out
        document.getElementById('cookie').style.display = 'none';
    }
}

function got_it(){
    // set the key 'cookie' to localStorage
    localStorage.setItem('cookie', 'true');
    // hide the cookie alert with animation which will move the alert to the right
    document.getElementById('cookie').style.transition = 'all 0.5s';
    document.getElementById('cookie').style.transform = 'translateX(100%)';
}