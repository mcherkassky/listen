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
            var params = { allowScriptAccess: "always" };
            swfobject.embedSWF( "http://www.youtube.com/v/" + youtube_id + "&enablejsapi=1&version=3&playerapiid=" + player_id,//ytplayer",
                player_id,
                "1", "1", "8",
                null, null, params, null, null);
        },
        search: function(song){
            var youtube_url = $q.defer(); //q promise callback dis some fancy ass shit
            $http({
                url:'/find/title/' + formatURL(song.title) +
                    '/album/' + formatURL(song.album.title) +
                    '/artist/' + formatURL(song.artist.name) +
                    '/duration/' + song.duration,
                method: 'GET'
            }).success(function(data){
                    youtube_url.resolve(data)
                });
            return youtube_url.promise;
        },
        play: function(player){
            $rootScope.PLAYER_STATUS = 'play';
            player.setVolume($rootScope.PLAYER_VOLUME);
            player.playVideo();

            $rootScope.PLAYER_TIME = Math.round(player.getCurrentTime());
            $rootScope.PLAYER_LENGTH = player.getDuration();

            //poll time in seconds
            $rootScope.getTime = setInterval(function(){
                $rootScope.$apply(function(){
                    $rootScope.PLAYER_TIME = Math.round(player.getCurrentTime());
                });
            },1000);
        },
        pause: function(player){
            $rootScope.PLAYER_STATUS = 'pause';
            player.pauseVideo();
            clearInterval($rootScope.getTime);
            $rootScope.getTime = null
        },
        seek: function(player, time){
            player.seekTo(time)
        }
    }
});