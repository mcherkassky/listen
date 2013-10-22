musicModule.factory('PlaylistFactory', function($resource){
    return $resource('user/:user_id/playlist/:id', {user_id: '@user_id', id: '@id'}, {
        edit: {method: 'PUT'}
    })
});