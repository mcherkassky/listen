musicModule.controller('PlaylistCtrl', function($rootScope, $q, $scope, $http, $timeout, PlaylistFactory, PlaylistSongFactory, UserFactory, MusicPlayer){
    //get playlists and associated songs
    $scope.user = UserFactory.get({},function(){
        $rootScope.music.playlists = PlaylistFactory.query({user_id: $scope.user._id.$oid});
        $rootScope.music.playlists.$promise.then(
            function(){
                for(var i = 0; i < $rootScope.music.playlists.length; i ++){
                    $rootScope.music.playlists[i].songs = PlaylistSongFactory.query({user_id:$scope.user._id.$oid,playlist_id:$rootScope.music.playlists[i]._id.$oid})
                    $rootScope.music.playlists[i].index = i;
                }
            }
        );

        $scope.new_playlist = function(){
            var playlist = {user_id: $scope.user._id.$oid};
            playlist = PlaylistFactory.save(playlist);

            $rootScope.music.playlists.push(playlist)
        }
    });

});