/**
 * Created by eduardo on 13/02/15.
 *
 * @param markers Markers list
 */
function initialize(markers) {
    // Center map in Brasilia
    var mapOptions = {
        zoom: 6,
        center: new google.maps.LatLng(-15.4647, -47.5547),
        mapTypeId: google.maps.MapTypeId.HYBRID
    };

    var map = new google.maps.Map(document.getElementById("map_canvas"), mapOptions);

    for (var i = 0; i < markers.length; i++) {

        var myLatlng = new google.maps.LatLng(
                markers[i]['latitude'],
                markers[i]['longitude']
        );

        // Change marker color
        if (markers[i]['category'] == undefined
            || markers[i]['category'] == null
            || markers[i]['category'].length == 0) {

            // Generate default Pin
            var mk = new google.maps.Marker({
                position: myLatlng,
                map: map,
                title: markers[i]['title']
            });
        } else {
            // Use category color
            var pinColor = markers[i]['category']['color'];
            // Remove # from color
            pinColor = pinColor.replace('#', '')
            var pinImage = new google.maps.MarkerImage("http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=%E2%80%A2|" + pinColor,
                new google.maps.Size(21, 34),
                new google.maps.Point(0,0),
                new google.maps.Point(10, 34));
            var pinShadow = new google.maps.MarkerImage("http://chart.apis.google.com/chart?chst=d_map_pin_shadow",
                new google.maps.Size(40, 37),
                new google.maps.Point(0, 0),
                new google.maps.Point(12, 35));

            var mk = new google.maps.Marker({
                position: myLatlng,
                map: map,
                title: markers[i]['title'],
                icon: pinImage,
                shadow: pinShadow
            });
        }

        loadWindow(mk, markers[i]);

    }

}

//window.onload = loadScript;


/**
 * Load HTML infoWindow
 *
 * @param marker Marker object
 * @param status status element with necessary attributes
 */
function loadWindow(marker, status) {
    var infowindow = new google.maps.InfoWindow({});

    google.maps.event.addListener(marker, 'click', function() {
        infowindow.open(marker.get('map'), marker);
        getHtml(status, infowindow);
    });
}

/**
 * Asynchronous load HTML data
 *
 * @param status Status object
 * @param infowindow Window object
 */
function getHtml(status, infowindow) {
    $.ajax({
        type: "GET",
        url: status['embed_url'],
        data: "",
        dataType: "text",
        success: function(html){
            infowindow.setContent(html);
        },
        error: function(){

            infowindow.setContent('<div class="alert alert-danger" role="alert">' +
              '<strong>Oh snap!</strong> Error embeding status.' +
            '</div>');

        },
        load: function(){
            infowindow.setContent('<div id="load-maps" class="loading"></div>');
        }
    });
}