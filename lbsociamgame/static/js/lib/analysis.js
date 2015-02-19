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
