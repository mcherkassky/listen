musicModule.controller('ArtistCtrl', function($rootScope, $q, $scope, $http, $timeout, MusicPlayer){
    $scope.results = false;
//    debugger;

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

    $scope.$watch('music.artists', function(oldVal,newVal){
        if($scope.music.artists.length > 0){
            var artist_ids = $scope.music.artists.map(function(element){return element.id});
            $http({
                url: '/artists/batch',
                method: 'POST',
                data: artist_ids
            }).success(function(data){
                    $scope.albums = data;


                    angular.element(document).ready(function () {
                        $timeout(function(){
                            $('.carousel').jcarousel({
                                scroll: 4,
                                itemFallbackDimension: 200
                            });
                            $scope.results = true;
                        },10)
                    });

                });
        }

    });
});