musicModule.controller('PlaylistCtrl', function($rootScope, $q, $scope, $http, $timeout, PlaylistFactory, PlaylistSongFactory,MusicPlayer){
    //get playlists and associated songs
    $rootScope.music.playlists = PlaylistFactory.query({user_id: 'hello'});
    $rootScope.music.playlists.$promise.then(
        function(){
            for(var i = 0; i < $rootScope.music.playlists.length; i ++){
                $rootScope.music.playlists[i].songs = PlaylistSongFactory.query({user_id:'hello',playlist_id:$rootScope.music.playlists[i]._id.$oid})
                $rootScope.music.playlists[i].index = i;
            }
        }
    );

    $scope.new_playlist = function(user_id){
        var playlist = {user_id: user_id};
        playlist = PlaylistFactory.save(playlist);

        $rootScope.music.playlists.push(playlist)
    }
});