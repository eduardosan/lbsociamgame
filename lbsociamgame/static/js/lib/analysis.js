/**
 * Created by eduardo on 12/02/15.
 */
function findTokenCategory(token, categories) {
    for (var i = 0; i < categories.length; i++ ) {
        if (token == categories[i]['default_token']) {
            return categories[i];
        } else if (categories[i]['tokens'] != 'undefined') {
            for (var j = 0; j < categories[i]['tokens'].length; j++) {
                if (token == categories[i]['tokens'][j]) {
                    return categories[i]
                }
            }
        }
        // If it gets here the token was not found
        return null;
    }
}

function statusLocations(result) {
    var markers = [];
    var evaluation = 0;
    var html = "";

    // Get results
    var status = result['status'];

    for (var i = 0; i < status['result_count']; i++ ) {
        // Load default data
        var title = "Status id " + status['results'][i]['_metadata']['id_doc'];
        var embed_url = "/embed/twitter/" + status['results'][i]['_metadata']['id_doc'];
        var status_id = status['results'][i]['_metadata']['id_doc'];

        // Consider only positive status
        if (( 'location' in status['results'][i]) && ('positives' in status['results'][i])) {
            if ('negatives' in status['results'][i]) {
                if (status['results'][i]['positives'] > status['results']['negatives']) {
                    markers.push({
                        'latitude': status['results'][i]['location']['latitude'],
                        'longitude': status['results'][i]['location']['longitude'],
                        'title': title,
                        'embed_url': embed_url,
                        'status_id': status_id,
                        'category': status['results'][i]['category']
                    });
                    evaluation = parseInt(status['results'][i]['positives']) - parseInt(status['results']['negatives'])
                }
            } else {
                markers.push({
                    'latitude': status['results'][i]['location']['latitude'],
                    'longitude': status['results'][i]['location']['longitude'],
                    'title': title,
                    'embed_url': embed_url,
                    'status_id': status_id,
                    'category': status['results'][i]['category']
                });
                evaluation = parseInt(status['results'][i]['positives']);
            }
        }

        // Add status visualization
        if (i < 10) {
            // Only 10 first status with more positives
            html += "<tr>";
            html += "<td>" + status['results'][i]['inclusion_datetime'] + "</td>";
            html += "<td>" + evaluation.toString() + "</td>";
            html += "<td>" + status['results'][i]['text'] + "</td>";
            html += "<td>" + status['results'][i]['origin'] + "</td>";
            html += "</tr>";
            $( '#status' ).append(html);
        }
    }

    return markers;
}

function loadTagclouds(route_url) {
    $.ajax({
        type: "GET",
        url: route_url,
        data: "",
        dataType: "html",
        success: function(result){
            $( '#load-tagcloud' ).hide();

            console.log(result);

            $( '#tagcloud' ).append(result);

            // Tagcloud configuration
            $.fn.tagcloud.defaults = {
              size: {start: 8, end: 12, unit: 'pt'},
              color: {start: '#cde', end: '#f52'}
            };

            $( '#tagcloud a').tagcloud();

        },
        error: function(result){
            console.log(result);
            alert("Error generating tagclouds");
        },
        load: function(){
            $( '#load-tagcloud' ).show();
        }
    });
}