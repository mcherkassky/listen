musicModule.controller('PlayerCtrl', function($rootScope, $scope, $timeout, MusicPlayer){
    $rootScope.PLAYER_SEEK = false;

    //initialize slider
    $('#slider').slider({
        max:0,
        min:0
    });

    //handle slider events
    $('.ui-slider-handle').mousedown(function(event){
        $rootScope.PLAYER_SEEK = true;
        $scope.pause();
    });

    $('#music-player').mouseup(function(event){
        if($rootScope.PLAYER_SEEK){
            $scope.seekTo($('#slider').slider('value'));
            $scope.play();
            $rootScope.PLAYER_SEEK = false;
        }
    });

    //MUSIC CONTROLS//
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

    //stop video
    $scope.stop = function(){
        MusicPlayer.stop(ytplayer);
    };

    //set volume
    $scope.setVolume = function(volume){
        MusicPlayer.setVolume(ytplayer, volume)
    };

    $rootScope.play_next = function(){
        if($rootScope.NEXT_READY){
            $rootScope.SONG_INDEX += 1;

            coverflow('albumflow').to($rootScope.SONG_INDEX);
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
                var youtube_url = $rootScope.SONGS[$rootScope.SONG_INDEX + 1].youtube_url;
                if(youtube_url != undefined){
                    MusicPlayer.loadVideo(youtube_url, "nextplayer")
                }
                else{
                    var promise = MusicPlayer.search($rootScope.SONGS[$rootScope.SONG_INDEX + 1]);
                    promise.then(function(url){
                        var youtube_url = url;
                        MusicPlayer.loadVideo(youtube_url, "nextplayer")
                    });
                }
            }
        }
    };
    $scope.play_previous = function(){
        if($rootScope.PLAYER_TIME > 5){
            $scope.seekTo(0)
        }
        else if($rootScope.PREV_READY){
            $rootScope.SONG_INDEX -= 1;
            coverflow('albumflow').to($rootScope.SONG_INDEX);
            MusicPlayer.pause(ytplayer);

            //some bomb ass logic
            $("#ytplayer").attr('id','tempplayer')
            $("#prevplayer").attr('id','ytplayer')
            $("#nextplayer").attr('id', 'prevplayer')
            $("#tempplayer").attr('id','nextplayer')
            $('#prevplayer').html(''); //remove everything from previous player

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
                var youtube_url = $rootScope.SONGS[$rootScope.SONG_INDEX - 1].youtube_url;
                if(youtube_url != undefined){
                    MusicPlayer.loadVideo(youtube_url, "prevplayer")
                }
                else{
                    var promise = MusicPlayer.search($rootScope.SONGS[$rootScope.SONG_INDEX - 1]);
                    promise.then(function(url){
                        var youtube_url = url;
                        MusicPlayer.loadVideo(youtube_url, "prevplayer")
                    });
                }
            }
        }
    };
    $rootScope.play_next_auto = function(){
        debugger;

        if($rootScope.NEXT_READY){
            $rootScope.SONG_INDEX += 1;

            coverflow('albumflow').to($rootScope.SONG_INDEX);
//            MusicPlayer.pause(ytplayer);
            clearInterval($rootScope.getTime);
            //some bomb ass logic
            $("#ytplayer").attr('id','tempplayer')
            $("#nextplayer").attr('id','ytplayer')
            $("#prevplayer").attr('id', 'nextplayer')
            $("#tempplayer").attr('id','prevplayer')
            $("#nextplayer").html(''); //remove everything from next player

            $rootScope.PREV_READY = true;
            $rootScope.NEXT_READY = false;
            $rootScope.getTime = null;

            MusicPlayer.play(ytplayer);
//            MusicPlayer.seek(prevplayer,0);

//            clearInterval($rootScope.getTime);
            var interval_times = 0;
            var volume_transition = setInterval(function(){
                MusicPlayer.setVolume(prevplayer, Math.max(0,100-interval_times));

//                MusicPlayer.setVolume(ytplayer, Math.max(100,interval_times));
                interval_times += 1;
            },30);


            var prev_player_duration = prevplayer.getDuration();
            var prev_player_time = setInterval(function(){
                if((prev_player_duration - prevplayer.getCurrentTime()) <= 0.5){
                    MusicPlayer.stop(prevplayer);
                    $rootScope.PLAYER_STATUS = 'play'; //override previous statement
//                    MusicPlayer.seek(prevplayer,0);
                    clearInterval(prev_player_time);
                    clearInterval(volume_transition);
                }
            },50);

            var temp_playing = $rootScope.currently_playing
            $rootScope.currently_playing = $rootScope.next_playing
            $rootScope.previous_playing = temp_playing
            $rootScope.next_playing = $rootScope.SONGS[$rootScope.SONG_INDEX + 1]

            if($rootScope.SONG_INDEX + 1 < $rootScope.SONGS.length){
                var youtube_url = $rootScope.SONGS[$rootScope.SONG_INDEX + 1].youtube_url;
                if(youtube_url != undefined){
                    MusicPlayer.loadVideo(youtube_url, "nextplayer")
                }
                else{
                    var promise = MusicPlayer.search($rootScope.SONGS[$rootScope.SONG_INDEX + 1]);
                    promise.then(function(url){
                        var youtube_url = url;
                        MusicPlayer.loadVideo(youtube_url, "nextplayer")
                    });
                }
            }
        }
//        $scope.play_next()
    }
});