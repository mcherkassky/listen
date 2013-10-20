musicModule.controller('AlbumCtrl', function($rootScope, $q, $scope, $http, $timeout, MusicPlayer){
    $scope.get_album_contents = function(album_id){
        $http({
            method: 'GET',
            url: '/albums/' + album_id
        }).success(function(data){
                $scope.music.songs = data;
            })
    };

    $scope.play_album_contents = function(album){
        var listener = $scope.$watch('music.songs', function(newVal, oldVal){
            if(newVal != oldVal){
//                $scope.load_videos($scope.music.up_next,0);
                $('#songs-tab').trigger('click');
                listener()
            }
        });
        $scope.get_album_contents(album.id);
    };
});
