function bindCaptchaBtnClick() {
    $("#captcha-btn").on("click", function (event) {
        var $this = $(this)
        var email = $("input[name='email']").val();
        var username = $("input[name='username']").val();
        if (!email) {
            alert("Colla: Please enter your e-mail first!");
            return;
        }
        // Send the request throw js：ajax：Async Javascript And XML
        $.ajax({
            url: "/user/captcha",
            method: "POST",
            data: {
                "email": email,
                "username": username
            },
            success: function (res) {
                var code = res['code']
                if (code === 200) {
                    // cancel the click event
                    $this.off("click")
                    // start the countdown
                    var countDown = 60;
                    var timer = setInterval(function () {
                        if (countDown > 0) {
                            $this.text(countDown + " s")
                        } else {
                            $this.text("Send");
                            // rebind the click event
                            bindCaptchaBtnClick();
                            // If the countdown is not needed, it needs to be cleared,
                            // otherwise it will continue to execute
                            clearInterval(timer)
                        }
                        countDown -= 1;
                    }, 1000)
                    alert("Captcha has been sent to your e-mail!");
                } else {
                    alert(res['message']);
                }
            }
        })
    })
}

function checkRegisterForm(){
    jQuery.validator.addMethod("itemPass", function (value, element) {
        var reg = /^\w+$/;
        return this.optional(element) || (reg.test(value));
    })

    jQuery.validator.addMethod("itemName", function (value, element) {
        var reg = /^[A-Za-z]+$/;
        return this.optional(element) || (reg.test(value));
    })

    $("#register_form").validate({
        rules: {
            username: {
                required: true,
                minlength: 3,
                maxLength: 20,
                itemName: true
            },
            password: {
                required: true,
                itemPass:true,
                minlength: 6,
                maxLength: 40
            },
            captcha: {
                required: false,
            },
            email: {
                required:true,
                email: true
            }
        },
        messages: {
            username: {
                required: "Please enter your username",
                minlength: "The user name is between 4 and 20 characters",
                itemName: "The user name can only be composed of letters"
            },
            password: {
                required: "Please enter your password",
                itemPass: "The password can only be composed of letters, numbers and underscores",
                minlength: "The password is between 6 and 40 characters"
            },
            email: {
                required: "Please enter your email",
                email: "Please enter a valid email address",
            }
        }
    })
}

// wait for the web page to load all elements
$(function () {
        bindCaptchaBtnClick();
        checkRegisterForm();
    }
)