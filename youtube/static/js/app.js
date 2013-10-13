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
});