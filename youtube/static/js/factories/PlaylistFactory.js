musicModule.factory('PlaylistFactory', function($resource){
    return $resource('user/:user_id/playlist/:id', {user_id: '@user_id', id: '@id'}, {
        edit: {method: 'PUT'}
    })
});

musicModule.factory('PlaylistSongFactory', function($resource){
    return $resource('user/:user_id/playlist/:playlist_id/song', {user_id: '@user_id', playlist_id: '@playlist_id'}, {
        edit: {method: 'PUT'}
    })
});

musicModule.factory('SongFactory', function($resource){
    return $resource('song/:song_id', {song_id: '@song_id'}, {
        edit: {method: 'PUT'}
    })
});

musicModule.factory('UserFactory', function($resource){
    return $resource('user',{})
});
