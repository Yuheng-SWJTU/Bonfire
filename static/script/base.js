function side() {
    var side = document.getElementById("side-menu");
    var container = document.getElementById("container-box");
    const cssSide = window.getComputedStyle(side);
    var svg = document.getElementById("shrink-svg");

    // detect the status of the side list
    if (cssSide.getPropertyValue("left") !== "-255px") {
        // side.style.width = "0px";
        side.style.left = "-255px";
        container.style.width = "100vw";
        svg.style.transform = "rotate(90deg)";
    } else {
        // side.style.width = "255px";
        console.log(side.style.left)
        side.style.left = "0px";
        svg.style.transform = "rotate(0deg)";
        if (document.body.clientWidth >= 750) {
            container.style.width = "calc(100vw - 255px)";
        } else {
            container.style.width = "100vw";
        }
    }
}


function side_post() {
    var side = document.getElementById("side-menu");
    var container = document.getElementById("container-box");
    const cssSide = window.getComputedStyle(side);
    var svg = document.getElementById("shrink-svg");
    var post_area = document.getElementById("post-area");

    // detect the status of the side list
    if (cssSide.getPropertyValue("left") !== "-255px") {
        // side.style.width = "0px";
        side.style.left = "-255px";
        container.style.width = "100vw";
        svg.style.transform = "rotate(90deg)";
        post_area.style.left = "0px";
        post_area.style.width = "100%";
    } else {
        // side.style.width = "255px";
        console.log(side.style.left)
        side.style.left = "0px";
        svg.style.transform = "rotate(0deg)";
        if (document.body.clientWidth >= 750) {
            container.style.width = "calc(100vw - 255px)";
            post_area.style.left = "255px";
            post_area.style.width = "calc(100vw - 255px)";
        } else {
            container.style.width = "100vw";
            post_area.style.left = "0px";
            post_area.style.width = "100%";
        }
    }
}

// click event for the animation of the button
function rotate() {
    var container = document.getElementsByClassName("side-list3")[0];
    var id = document.getElementById("side-title-btn2");
    if (id.style.transform === "rotate(0deg)") {
        id.style.transform = "rotate(90deg)";
    } else {
        container.style.height = "calc(100vh - 485px) !important";
        id.style.transform = "rotate(0deg)";
    }
}