musicModule.controller('FeaturedCtrl', function($rootScope, $q, $scope, $http, $timeout, MusicPlayer){
    //get data for featured page
    $http({
        url: '/featured',
        method: 'GET'
    }).success(function(data){
            $rootScope.music.featured = data;
            $timeout(function(){
                $scope.refreshTiles('#featured',10)
                console.log('ok')

            },500)

        });
});