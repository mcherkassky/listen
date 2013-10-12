musicModule.controller('SearchCtrl', function($rootScope, $q, $scope, $http, $timeout, MusicPlayer){
    $scope.format_to_time = function(value){
        var hours = Math.floor(value / 3600);
        var minutes = Math.floor(value % 3600 / 60);
        var seconds = Math.floor(value % 3600 % 60);
        return ((hours>0?hours+":":"")+(minutes>0?(hours>0&&minutes<10?"0":"")+minutes + ":":"0:")+(seconds<10?"0":"")+seconds);
    };

    $scope.loading = false;
    $scope.results = false;
    $rootScope.currently_playing = undefined;
    $scope.playlist_songs = [];

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

    };

    $scope.get_album_contents = function(album_id){
        console.log(album_id);
        $http({
            method: 'GET',
            url: '/albums/' + album_id
        }).success(function(data){
                console.log(data);
                $scope.songs = data;
            })
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
                            $scope.songs = data['songs'];
                            $scope.albums = data['albums'];
                            $scope.artists = data['artists'];

                            if($scope.albums.length<5){
                                var song_albums = $scope.songs.map(function(element){return element.album})
                                song_albums = getUniques(song_albums).sort(compareListeners).reverse();
                                song_albums.slice(0,Math.min(5-$scope.albums.length,song_albums.length)).map(function(element){
                                    $scope.albums.push(element)
                                });
                            }
                            if($scope.artists.length<5){
                                var song_artists = $scope.songs.map(function(element){return element.artist})
                                song_artists = getUniques(song_artists).sort(compareListeners).reverse();
                                song_artists.slice(0,Math.min(5-$scope.artists.length,song_artists.length)).map(function(element){
                                    $scope.artists.push(element)
                                });
                            }
                        }
                        $scope.loading = false;
                        $scope.results = true;
                        console.log(data);
                    })
                }
            },1000);
        }

    });
});