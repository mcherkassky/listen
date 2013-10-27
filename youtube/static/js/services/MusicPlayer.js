musicModule.service('MusicPlayer', function($rootScope, $timeout, $q, $http){
    return {
        loadVideo: function(youtube_id, player_id){
            var self = this;

            //watch youtube js api handlers
            window.onYouTubePlayerReady = function(playerId) {
                if (playerId == "ytplayer") {
                    self.play(ytplayer)
                }
                else if (playerId == 'prevplayer'){
                    $rootScope.PREV_READY = true
                }
                else if (playerId == 'nextplayer'){
                    $rootScope.NEXT_READY = true
                }
            };

            //set up embedded video
            var params = { allowScriptAccess: "always", 'controls': 0 };


            swfobject.embedSWF( "http://www.youtube.com/v/" + youtube_id + "&enablejsapi=1&version=3&playerapiid=" + player_id,//ytplayer",
                player_id,
                "290", '210', "8",
                null, null, params, null, null);

            $('#ytplayer').parent().css("z-index",'1');
            $('#prevplayer').parent().css("z-index",'-100');
            $('#nextplayer').parent().css("z-index",'-100');



//            //load slider
//            $timeout(function(){
//                $('#slider').slider({
//                    min: 0,
//                    max: $rootScope.PLAYER_LENGTH
//                });
//            },10);



            $rootScope.$watch('PLAYER_TIME', function(){
                if(player_id == 'ytplayer'){
                    if($(ytplayer).html() != ''){
                        $('#slider').slider('value',$rootScope.PLAYER_TIME);
                        var time_left = ytplayer.getDuration() - ytplayer.getCurrentTime();
                        if(time_left <= 3){
                            $rootScope.play_next_auto()
                        }
                    }
                }

            })

        },
        search: function(song){
            var youtube_url = $q.defer(); //q promise callback dis some fancy ass shit
            $http({
                url:'/find/title/' + formatURL(song.title) +
                    '/album/' + formatURL(song.album) +
                    '/artist/' + formatURL(song.artist) +
                    '/duration/' + song.duration,
                method: 'GET'
            }).success(function(data){
                    youtube_url.resolve(data)
                });
            return youtube_url.promise;
        },
        play: function(player){
            clearInterval($rootScope.getTime);

            $rootScope.PLAYER_STATUS = 'play';
            player.setVolume($rootScope.PLAYER_VOLUME);
            player.playVideo();

            $rootScope.PLAYER_TIME = Math.round(player.getCurrentTime());
            $rootScope.PLAYER_LENGTH = player.getDuration();

            $('#slider').slider({
                min: 0,
                max: $rootScope.PLAYER_LENGTH
            });

            //poll time in seconds
            $rootScope.getTime = setInterval(function(){
                $rootScope.$apply(function(){
                    $rootScope.PLAYER_TIME = Math.round(player.getCurrentTime());
                    console.log($rootScope.PLAYER_TIME)
                });
            },1000);
        },
        pause: function(player){
            $rootScope.PLAYER_STATUS = 'pause';
            player.pauseVideo();
            clearInterval($rootScope.getTime);
            $rootScope.getTime = null
        },
        stop: function(player){
            $rootScope.PLAYER_STATUS = 'stop';
            player.pauseVideo();
            player.seekTo(0);
        },
        seek: function(player, time){
            player.seekTo(time)
        },
        setVolume: function(player, volume){
            player.setVolume(volume);
        }
    }
});