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
    $scope.playlist_songs = [];
    $scope.youtube_results = [];

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

        if(coverflow('albumflow').config == null){
            $rootScope.coverflow();
            $timeout(function(){
                coverflow('albumflow').to(index);
            },100)
        }
        else{
            coverflow('albumflow').to(index);
        }
    };

    $scope.get_album_contents = function(album_id){

        $http({
            method: 'GET',
            url: '/albums/' + album_id
        }).success(function(data){
                console.log(data);
                $scope.songs = data;
                $scope.all_songs.playlist = data;
//                $rootScope.coverflow()
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
                            $rootScope.all_songs.playlist = data['songs'];
//                            $rootScope.coverflow();
                            $scope.songs = data['songs'];
                            $scope.albums = data['albums'];
                            $scope.artists = data['artists'];
                        }
                        $scope.loading = false;
                        $scope.results = true;
                    })
                }
            },1000);
        }

    });
});