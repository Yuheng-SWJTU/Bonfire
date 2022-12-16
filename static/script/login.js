function checkRegisterForm(){
    jQuery.validator.addMethod("itemPass", function (value, element) {
        var reg = /^\w+$/;
        return this.optional(element) || (reg.test(value));
    })

    jQuery.validator.addMethod("itemName", function (value, element) {
        var reg = /^[A-Za-z]+$/;
        return this.optional(element) || (reg.test(value));
    })

    $("#login_form").validate({
        rules: {
            password: {
                required: true,
                itemPass:true,
                minlength: 6,
                maxLength: 40
            },
            email: {
                required:true,
                email: true
            }
        },
        messages: {
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
    checkRegisterForm();
    // if remember me is checked, set the localStorage
    if ($('input[name="remember"]:checked').val() === 'rememberme') {
        console.log("remember me is checked");
        localStorage.setItem('rememberme', 'true');
        localStorage.setItem('email', $('#email').val());
        localStorage.setItem('password', $('#password').val());
    }
})