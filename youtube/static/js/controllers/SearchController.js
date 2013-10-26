musicModule.controller('SearchCtrl', function($rootScope, $q, $scope, $http, $timeout, MusicPlayer){
    $scope.test = function(element){
        console.log(element)
    };

    $scope.search_toggle = function(){
        $scope.search_toggle_bool = !$scope.search_toggle_bool;
        $scope.search_query = '';
        $scope.youtube_query = '';
    };

    $scope.loading = false;
    $scope.results = false;
    $scope.show_youtube_results = false;
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
                    'gutter': 20
                });
        },10)
    };
    //need this don't delete
    $scope.refreshTiles = function(container_id){
        $timeout(function(){
            $(container_id).masonry({
                'gutter':20
            })
        },10)

    };

    $scope.refreshCarousel = function(container_id){
        $timeout(function(){
            $(container_id).jcarousel({
//                visible:4,
//                scroll: 4,
//                itemFallbackDimension: 200
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
                $scope.show_youtube_results = false;
            }


            if (searchTimeout) $timeout.cancel(searchTimeout);
            searchText = newVal;

            searchTimeout = $timeout(function(){
                if($scope.search_query==""){
                    $scope.loading=false;
                    $scope.results=true;
//                    $scope.results = false;
                }
                else{
                    $('.results-table').block({ message: '<h5>Loading</h5><br><img height=45 width=45 src="/static/img/ajax-loader.gif">' })

                    $http.get('/search/' + searchText).success(function(data){
                        if(data != undefined){
                            if($('#albums').css('position') == 'relative'){
                                $('#albums').masonry('destroy')
                            }
//                            if(data['songs'].length)
//                            if(data['songs'].length < 25){
//                                data['songs'] = data['songs'].concat(buildArray(20-data['songs'].length))
//                            }


                            $scope.music.songs = data['songs'];
                            $scope.music.albums = data['albums'];
                            $scope.music.artists = data['artists'];

                            if($scope.music.songs.length == 0){
                                $http.get('/find/' + searchText).success(function(data){
                                    $scope.music.youtube_results = data;
                                })
                                $scope.show_youtube_results = true;
                            }
                            else{
                                $scope.show_youtube_results = false;
                                $scope.results = true;
                                tile_images('#albums');
                            }

                            //selecatble song elements
                            $('.selectable').multiSelect({
                                unselectOn: 'body',
                                keepSelection: false
                            });
                        }
                        $('.results-table').unblock()
                        $scope.loading = false;
                        $scope.contextMenu()
                    })
                }
            },1000);
        }

    });
});