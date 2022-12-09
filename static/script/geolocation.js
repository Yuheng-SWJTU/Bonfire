//--------------------------------------------------------------------------------------------------------

// This part of JS is independent of the rest,
// and this part is only responsible for the positioning acquisition function in photo.html

// WARNING:
// The location service is provided by Baidu. Turning on the VPN during the test or the network
// speed is too slow will cause the location to fail.
// After opening the file locally, the browser console will report an error. This is because the
// Baidu positioning API does not allow cross-domain access, and it is not an error in the Javascript code.

// If the browser alerts the key has expired, please contact the web creator Yuheng LIU:2964992240 to get
// a new access key.

//--------------------------------------------------------------------------------------------------------

var geolocation = new BMap.Geolocation();
var gc = new BMap.Geocoder();

window.onload = function (){
    geolocation.getCurrentPosition(function (r) {
            var blank = document.getElementById("location")
            if (this.getStatus() === BMAP_STATUS_SUCCESS) {
                var pt = r.point;
                gc.getLocation(pt, function (rs) {
                    var addComp = rs.addressComponents;
                    try{
                        blank.innerHTML = addComp.city.replace("市", "");
                    } catch (e) {
                        blank.innerHTML = addComp.city;
                    }
                });
            } else {
                switch (this.getStatus()) {
                    case 2:
                        alert('Location service failed, please check your network connection and try again.');
                        break;
                    case 3:
                        alert('Location service failed, please check your network connection and try again.');
                        break;
                    case 4:
                        alert('Location service failed, please check your network connection and try again.');
                        break;
                    case 5:
                        alert('Location service failed, please check your network connection and try again.');
                        break;
                    case 6:
                        alert('Location service failed, please check your network connection and try again.');
                        break;
                    case 7:
                        alert('Location service failed, please check your network connection and try again.');
                        break;
                    case 8:
                        alert('Location service failed, please check your network connection and try again.');
                        break;

                }
            }

        },
        {enableHighAccuracy: true}
    )
}
