musicModule.controller('ArtistCtrl', function($rootScope, $q, $scope, $http, $timeout, MusicPlayer){
    $scope.results = false;
//    debugger;


    $scope.$watch('music.artists', function(oldVal,newVal){

        if($scope.music.artists.length > 0){
            var artist_ids = $scope.music.artists.map(function(element){return element.id});
            $http({
                url: '/artists/batch',
                method: 'POST',
                data: artist_ids
            }).success(function(data){
                    $scope.albums = data;


                    angular.element(document).ready(function () {
                        $timeout(function(){
                            $('.carousel').jcarousel({
                                visible: 6,
                                scroll: 6,
                                itemFallbackDimension: 150
                            })
                            $scope.results = true;
                        },10)
                    });

                });
        }

    });
});