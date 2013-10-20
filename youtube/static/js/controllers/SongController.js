musicModule.controller('SongCtrl', function($rootScope, $q, $scope, $http, $timeout, MusicPlayer){
    var load_song_to_container = function(song, player_id){
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
            load_song_to_container(songs[index+1], "nextplayer")
            $rootScope.next_playing = songs[index+1]
        }
        if(index != 0){
            load_song_to_container(songs[index-1], "prevplayer")
            $rootScope.previous_playing = songs[index-1]
        }
    };

    $rootScope.load_videos = function(songs, index){
        if($rootScope.currently_playing == songs[index])
            return;
        if($rootScope.PLAYER_STATUS == 'play')
            MusicPlayer.pause(ytplayer);

        //update song index for all controllers
        $rootScope.SONGS = songs;
        $rootScope.SONG_INDEX = index;

        $rootScope.getTime = null;
        $rootScope.PLAYER_TIME = 0;

        load_song_to_container(songs[index], "ytplayer");
        $rootScope.PLAYER_STATUS = 'loaded';
        $rootScope.currently_playing = songs[index];

        if(index != songs.length - 1){
            load_song_to_container(songs[index+1], "nextplayer")
            $rootScope.next_playing = songs[index+1]
        }
        if(index != 0){
            load_song_to_container(songs[index-1], "prevplayer")
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


});