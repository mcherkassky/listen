musicModule.controller('SearchCtrl', function($rootScope, $q, $scope, $http, $timeout, MusicPlayer){
    $scope.format_to_time = function(value){
        var hours = Math.floor(value / 3600);
        var minutes = Math.floor(value % 3600 / 60);
        var seconds = Math.floor(value % 3600 % 60);
        return ((hours>0?hours+":":"")+(minutes>0?(hours>0&&minutes<10?"0":"")+minutes + ":":"0:")+(seconds<10?"0":"")+seconds);
    };

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
    }

    var load_video_to_container = function(song, player_id){
        if(song.youtube_url != undefined){
            MusicPlayer.loadVideo(song.youtube_url, player_id);
        }
        else{
            var promise = MusicPlayer.search(song);
            promise.then(function(url){
                var youtube_url = url;
                MusicPlayer.loadVideo(youtube_url, player_id)
            });
        }
    };

    //loading for up next
    $scope.dynamic_load_videos = function(songs, index){
        //update song index for all controllers
        $rootScope.SONGS = songs;
        $rootScope.SONG_INDEX = index;

        if(index != songs.length - 1){
            load_video_to_container(songs[index+1], "nextplayer")
            $rootScope.next_playing = songs[index+1]
        }
        if(index != 0){
            load_video_to_container(songs[index-1], "prevplayer")
            $rootScope.previous_playing = songs[index-1]
        }
    };

    $scope.load_videos = function(songs, index){
        if($rootScope.currently_playing == songs[index])
            return;
        if($rootScope.PLAYER_STATUS == 'play')
            MusicPlayer.pause(ytplayer);


        //update song index for all controllers
        $rootScope.SONGS = songs;
        $rootScope.SONG_INDEX = index;

        $rootScope.getTime = null;
        $rootScope.PLAYER_TIME = 0;

        load_video_to_container(songs[index], "ytplayer");

        $rootScope.PLAYER_STATUS = 'loaded';
        $rootScope.currently_playing = songs[index];

        if(index != songs.length - 1){
            load_video_to_container(songs[index+1], "nextplayer")
            $rootScope.next_playing = songs[index+1]
        }
        if(index != 0){
            load_video_to_container(songs[index-1], "prevplayer")
            $rootScope.previous_playing = songs[index-1]
        }

        $rootScope.music.up_next = songs;
        $rootScope.is_up_next_playing = false;

        if(coverflow('albumflow').config == null){
            $rootScope.coverflow()

        }
        else{
            if(songs == coverflow('albumflow').config.playlist){
                coverflow('albumflow').to(index);
            }
            else{
                $rootScope.coverflow()
            }
        }
    };

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
                $scope.load_videos($scope.music.up_next,0);
                $('#songs-tab').trigger('click');
                listener()
            }
        })
        $scope.get_album_contents(album.id);

    };

    $scope.refreshTiles = function(container_id){
        $timeout(function(){
            $(container_id).masonry({
                'gutter':10
            })
        },10)

    };

    var tile_images = function(container_id){
        $timeout(function(){
                $(container_id).masonry({
                    'gutter': 10
                });
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
                        tile_images('#albums')
                    })
                }
            },1000);
        }

    });
});