/**
 * Created by eduardo on 13/02/15.
 */
function initialize(markers) {
    // Center map in Brasilia
    var mapOptions = {
        zoom: 8,
        center: new google.maps.LatLng(-15.4647, -47.5547),
        mapTypeId: google.maps.MapTypeId.HYBRID
    };

    var map = new google.maps.Map(document.getElementById("map_canvas"), mapOptions);

    for (var i = 0; i < markers.length; i++) {
        var myLatlng = new google.maps.LatLng(
                markers[i]['latitude'],
                markers[i]['longitude']
        );
        var mk = new google.maps.Marker({
            position: myLatlng,
            map: map,
            title: markers[i]['title']
        });

    }

}

//window.onload = loadScript;