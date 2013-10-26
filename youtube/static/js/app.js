'use strict';

var buildArray = function(n){
    return Array(n).join(1).split('').map(function(){return {}});
};

var musicModule = angular.module('musicModule',['ngResource','ui.bootstrap','ngDragDrop'],function($interpolateProvider){
    $interpolateProvider.startSymbol('[[');
    $interpolateProvider.endSymbol(']]')
});

musicModule.run(function($rootScope, MusicPlayer, PlaylistFactory, PlaylistSongFactory, UserFactory, SongFactory,$timeout, $http){
    //get current user
    $rootScope.user = UserFactory.get({},function(){});


    $rootScope.PLAYER_STATUS = null;
    $rootScope.PLAYER_VOLUME = 100;
    $rootScope.PLAYER_TIME = 0;
    $rootScope.PLAYER_LENGTH = 0;
    $rootScope.PLAYER_SEEK = null;
    $rootScope.PLAYER_MUTE = false;

    $rootScope.SONGS = null;
    $rootScope.SONG_INDEX = 0;

    $rootScope.search_toggle_bool = true;
    $rootScope.is_up_next_playing = undefined;

    $rootScope.format_to_time = function(value){
        if(value){
            var hours = Math.floor(value / 3600);
            var minutes = Math.floor(value % 3600 / 60);
            var seconds = Math.floor(value % 3600 % 60);
            return ((hours>0?hours+":":"")+(minutes>0?(hours>0&&minutes<10?"0":"")+minutes + ":":"0:")+(seconds<10?"0":"")+seconds);
        }
        return ""

    };

    $rootScope.music = {
        up_next:[],
        songs:buildArray(25),
        albums:[],
        artists:[],
        youtube_results:[],
        playlists: []
    };
    debugger;

    var timeout;
    $rootScope.coverflow = function(){
        coverflow('albumflow').remove();
        coverflow('albumflow').setup({
            //mode: "flash",
            flash: "http://luwes.co/js-cover-flow/coverflow.swf",
            playlist: $rootScope.music.up_next,
            width: '100%',
            item:$rootScope.SONG_INDEX,
            height: 200,
            y: -20,
            backgroundcolor: "ffffff",
            coverwidth: 150,
            coverheight: 130,

            fixedsize: true,
            textoffset: 50,
            textstyle: ".coverflow-text{color:#34495e;text-align:center;font-family:Lato, sans-serif;} .coverflow-text h1{font-size:14px;font-weight:normal;line-height:21px;} .coverflow-text h2{font-size:11px;font-weight:normal;} .coverflow-text a{color:#34495e;}"
        })
        .on('ready', function() {
            this.on('focus', function(index) {
                if(timeout){
                    $timeout.cancel(timeout)
                }
                timeout = $timeout(function(){
                    coverflow('albumflow').to($rootScope.SONG_INDEX);
                },3500);
//                    document.getElementById('focusindex').innerHTML = index;
            });
            this.on('click', function(index, link) {
//                    document.getElementById('clickindex').innerHTML = index;
//
//                    console.log(link);
//                    if (link) {
//                            window.open(link, '_blank');
//                    }
            });
        });
    };

    $rootScope.contextMenu = function(){
//        var cachedHandler = null;
//        // disable
//        cachedHandler = $('#demo2').data('events').contextmenu[0].handler;
//        $('.context-menu').unbind('contextmenu', cachedHandler);
        // enable


//        debugger;

        $(function(){
            $.contextMenu({
                selector: '.context-menu',
                build: function($trigger, e){
                    var playlist_options = {};
                    for(var i = 0; i < $rootScope.music.playlists.length; i ++){
                        playlist_options[i] = {name:$rootScope.music.playlists[i].name,
                                                                          id: $rootScope.music.playlists[i]._id.$oid}
                    }
                    return{
                        callback: function(key, options) {
                            if(key == 'play'){
                                $rootScope.load_videos($rootScope.music.songs,options.$trigger.data('index'));
                            }
                            else if(key == "queue"){
                                debugger;
                            }
                            else if(Object.keys(playlist_options).indexOf(key) >= 0){
                                var playlist = PlaylistFactory.get({user_id:$rootScope.user._id.$oid, id:playlist_options[key].id}, function(){
                                    playlist.song_ids = playlist.song_ids.map(function(element){return element.$oid});
                                    playlist.song_ids.push(options.$trigger.data('id'));
                                    playlist.user_id = $rootScope.user._id.$oid;
                                    playlist.id = playlist._id.$oid
                                    playlist.$save()
                                    var song = SongFactory.get({song_id:options.$trigger.data('id')}, function(){
                                        if($rootScope.music.playlists[Object.keys(playlist_options).indexOf(key)].songs == undefined){
                                            $rootScope.music.playlists[Object.keys(playlist_options).indexOf(key)].songs = []
                                        }
                                        $rootScope.music.playlists[Object.keys(playlist_options).indexOf(key)].songs.push(song)
                                    });
                                })
                            }

                        },
                        items: {
                            "play": {name: "Play", icon:'play'},
                            "next": {name: "Play Up Next"},
                            "queue": {name: "Add To Queue"},
                            "playlist": {
                                name:"Add To Playlist",
                                items: playlist_options
                            }
                        }
                    }
                }

            });
        });
    }



});