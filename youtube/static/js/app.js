'use strict';

var musicModule = angular.module('musicModule',['ui.bootstrap','uiSlider','ngDragDrop'],function($interpolateProvider){
    $interpolateProvider.startSymbol('[[');
    $interpolateProvider.endSymbol(']]')
});

musicModule.run(function($rootScope){
    $rootScope.PLAYER_STATUS = null;
    $rootScope.PLAYER_VOLUME = 50;
    $rootScope.PLAYER_TIME = 0;
    $rootScope.PLAYER_LENGTH = 0;
    $rootScope.PLAYER_SEEK = null;

    $rootScope.SONGS = null;
    $rootScope.SONG_INDEX = 0;

    $rootScope.search_toggle_bool = true;

    $rootScope.format_to_time = function(value){
        var hours = Math.floor(value / 3600);
        var minutes = Math.floor(value % 3600 / 60);
        var seconds = Math.floor(value % 3600 % 60);
        return ((hours>0?hours+":":"")+(minutes>0?(hours>0&&minutes<10?"0":"")+minutes + ":":"0:")+(seconds<10?"0":"")+seconds);
    };

    $rootScope.all_songs = {
        playlist:[]
    };

    $rootScope.coverflow = function(){
        coverflow('albumflow').remove();
        coverflow('albumflow').setup({
            //mode: "flash",
            flash: "http://luwes.co/js-cover-flow/coverflow.swf",
            playlist: $rootScope.all_songs.playlist,
            width: '100%',
            height: 250,
            y: -20,
            backgroundcolor: "ffffff",
            coverwidth: 180,
            coverheight: 150,
            fixedsize: true,
            textoffset: 50,
            textstyle: ".coverflow-text{color:#000000;text-align:center;font-family:Arial Rounded MT Bold,Arial;} .coverflow-text h1{font-size:14px;font-weight:normal;line-height:21px;} .coverflow-text h2{font-size:11px;font-weight:normal;} .coverflow-text a{color:#0000EE;}"

        })
    }

});