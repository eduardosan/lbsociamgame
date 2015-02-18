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

        var mk = new google.maps.Marker({
            position: myLatlng,
            map: map,
            title: markers[i]['title']
        });

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
 * @param embed_url URL to request embeded data
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