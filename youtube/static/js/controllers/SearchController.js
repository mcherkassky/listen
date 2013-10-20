musicModule.controller('SearchCtrl', function($rootScope, $q, $scope, $http, $timeout, MusicPlayer){
    $scope.search_toggle = function(){
        $scope.search_toggle_bool = !$scope.search_toggle_bool;
        $scope.search_query = '';
        $scope.youtube_query = '';
    };

    $scope.loading = false;
    $scope.results = false;
    $rootScope.currently_playing = undefined;

    $scope.youtube_results = [];

    // handles up next droppable
    $rootScope.up_next = function(){
        if($rootScope.is_up_next_playing == undefined){
            $scope.load_videos($rootScope.music.up_next, 0);
            $rootScope.is_up_next_playing = true;
        }
        else if($rootScope.is_up_next_playing){
            $rootScope.coverflow();
            $scope.dynamic_load_videos($rootScope.music.up_next, $rootScope.SONG_INDEX)
        }
        else{
            $rootScope.music.up_next = [$rootScope.music.up_next[$rootScope.music.up_next.length-1]]; //replace with last element
//            $rootScope.is_up_next_playing = true;
            $scope.load_videos($rootScope.music.up_next, 0);
            $rootScope.is_up_next_playing = true;
        }
    };

    var tile_images = function(container_id){
        $timeout(function(){
                $(container_id).masonry({
                    'gutter': 10
                });
        },10)
    };
    //need this don't delete
    $scope.refreshTiles = function(container_id){
        $timeout(function(){
            $(container_id).masonry({
                'gutter':10
            })
        },10)

    };

    //watching search bar
    var searchText = " ", searchTimeout;
    $scope.$watch('search_query', function(newVal, oldVal){
        if(newVal != undefined){
            if(newVal!=""){
                $scope.loading = true;
                $scope.comments_show = false;
                $scope.results = false;
            }

            if (searchTimeout) $timeout.cancel(searchTimeout);
            searchText = newVal;

            searchTimeout = $timeout(function(){
                if($scope.search_query==""){
                    $scope.loading=false;
                    $scope.results=false;
                    $scope.results = false;
                }
                else{
                    $http.get('/search/' + searchText).success(function(data){
                        if(data != undefined){
//                            $rootScope.all_songs.playlist = data['songs'];
//                            $rootScope.coverflow();
//                            $('#albums').masonry('destroy')
                            if($('#albums').css('position') == 'relative'){
                                $('#albums').masonry('destroy')
                            }
                            $scope.music.songs = data['songs'];
                            $scope.music.albums = data['albums'];
                            $scope.music.artists = data['artists'];
                        }
                        $scope.loading = false;
                        $scope.results = true;
                        tile_images('#albums');
                        $scope.contextMenu()
                    })
                }
            },1000);
        }

    });
});