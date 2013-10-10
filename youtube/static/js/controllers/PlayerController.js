musicModule.controller('PlayerCtrl', function($rootScope, $scope, $timeout, MusicPlayer){
    $rootScope.PLAYER_SEEK = false;
    $('.pointer').mousedown(function(){
        $rootScope.PLAYER_SEEK = true;
        $scope.pause();
    });

    $('#music-player').mouseup(function(){
        if($rootScope.PLAYER_SEEK){
            $scope.seekTo($rootScope.PLAYER_TIME);
            $scope.play();
            $rootScope.PLAYER_SEEK = false;
        }
    });



    $scope.$watch('PLAYER_TIME', function(newVal, oldVal){
        var time_left = $rootScope.PLAYER_LENGTH - newVal;
        console.log(time_left)
        if(time_left == 3){
            console.log('im switching')
            $scope.play_next_auto()
        }
    });

    //CONTROLS//
    //play video
    $scope.play = function(){
        MusicPlayer.play(ytplayer);
    };
    //seek to video time
    $scope.seekTo = function(time){
        MusicPlayer.seek(ytplayer, time);
    };
    //pause video
    $scope.pause = function(){
        MusicPlayer.pause(ytplayer);
    };
    $scope.play_next = function(){
        if($rootScope.NEXT_READY){
            $rootScope.SONG_INDEX += 1;
            MusicPlayer.pause(ytplayer);

            //some bomb ass logic
            $("#ytplayer").attr('id','tempplayer')
            $("#nextplayer").attr('id','ytplayer')
            $("#prevplayer").attr('id', 'nextplayer')
            $("#tempplayer").attr('id','prevplayer')
            $(nextplayer).html(''); //remove everything from next player

            $rootScope.PREV_READY = true;
            $rootScope.NEXT_READY = false;
            $rootScope.getTime = null;
            MusicPlayer.play(ytplayer);
            MusicPlayer.seek(prevplayer,0);


            var temp_playing = $rootScope.currently_playing
            $rootScope.currently_playing = $rootScope.next_playing
            $rootScope.previous_playing = temp_playing
            $rootScope.next_playing = $rootScope.SONGS[$rootScope.SONG_INDEX + 1]

            if($rootScope.SONG_INDEX + 1 < $rootScope.SONGS.length){
                var promise = MusicPlayer.search($rootScope.SONGS[$rootScope.SONG_INDEX + 1]);
                promise.then(function(url){
                    var youtube_url = url;
                    MusicPlayer.loadVideo(youtube_url, "nextplayer")
                });
            }
        }
    };
    $scope.play_previous = function(){
        if($rootScope.PREV_READY){
            $rootScope.SONG_INDEX -= 1;
            MusicPlayer.pause(ytplayer);

            //some bomb ass logic
            $("#ytplayer").attr('id','tempplayer')
            $("#prevplayer").attr('id','ytplayer')
            $("#nextplayer").attr('id', 'prevplayer')
            $("#tempplayer").attr('id','nextplayer')
            $(prevplayer).html(''); //remove everything from previous player

            $rootScope.PREV_READY = false;
            $rootScope.NEXT_READY = true;
            $rootScope.getTime = null;
            MusicPlayer.play(ytplayer);
            MusicPlayer.seek(nextplayer,0);

            var temp_playing = $rootScope.currently_playing
            $rootScope.currently_playing = $rootScope.previous_playing;
            $rootScope.next_playing = temp_playing
            $rootScope.previous_playing = $rootScope.SONGS[$rootScope.SONG_INDEX - 1];

            if($rootScope.SONG_INDEX > 0){
                var promise = MusicPlayer.search($rootScope.SONGS[$rootScope.SONG_INDEX - 1]);
                promise.then(function(url){
                    var youtube_url = url;
                    MusicPlayer.loadVideo(youtube_url, "prevplayer")
                });
            }
        }
    };
    $scope.play_next_auto = function(){
        $scope.play_next()
    }
});