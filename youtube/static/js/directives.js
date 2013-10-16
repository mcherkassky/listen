musicModule.directive('timeify', function($timeout,$http){
    return{
        link: function(scope, element){
            $timeout(function(){
                console.log(element.html())
                var value = element.html();
                var hours = Math.floor(value / 3600);
                var minutes = Math.floor(value % 3600 / 60);
                var seconds = Math.floor(value % 3600 % 60);
                element.html(((hours>0?hours+":":"")+(minutes>0?(hours>0&&minutes<10?"0":"")+minutes + ":":"0:")+(seconds<10?"0":"")+seconds))
            })
        }
    }
});

musicModule.directive('dropdown', function($document, $timeout, $http) {
    return {
      restrict: 'A',
      replace: true,
      transclude: true,
      template: '<span ng-init="show_menu = false">' +
                  '<form style="border:0" class="navbar-search pull-right">' +
                  '<input ng-show="search_toggle_bool" style="height:10px;margin-bottom:0" ng-model="search_query" type="text" class="search span3">' +
                  '<input ng-show="!search_toggle_bool" style="height:10px;margin-bottom:0" ng-model="youtube_query" type="text" class="search span3">' +
                  '<span ng-click="search_toggle()" ng-show="search_toggle_bool"><div class="icon-search"></div></span>' +
                  '<span ng-click="search_toggle()" ng-show="!search_toggle_bool"><div class="icon-youtube-sign"></div></span>' +
                  '</form>' +
                  '<span ng-show="show_menu" class="dropdownMenu" ng-style="menuStyle" ng-transclude></span>' +
                  '</span>',
      link: function(scope, elm, attrs) {
        var searchText = " ", searchTimeout;
        scope.$watch('youtube_query', function(newVal, oldVal){
            console.log(newVal)
            if(newVal != undefined){
                if(newVal!=""){
                    scope.loading = true;
                    scope.show_menu = false;
                    scope.results = false;
                }

                if (searchTimeout) $timeout.cancel(searchTimeout);
                searchText = newVal;
                searchTimeout = $timeout(function(){
                    if(scope.youtube_query==""){
                        console.log('yo')
                        scope.loading=false;
                        scope.results=false;
                        scope.results = false;
                    }
                    else{
                        $http.get('/find/' + searchText).success(function(data){
                            scope.youtube_results = data;
                            console.log(data);
                            scope.show_menu=true
                        })
                    }
                },1000);
        }

    });
        scope.menuStyle = { 'position': 'absolute' };

        elm.bind('mousedown', function() {
          // mousedown event is called earlier than click event
          scope.menuStyle['left'] =  elm.prop('offsetLeft') + 'px';
          scope.menuStyle['top'] =  (elm.prop('offsetTop') + elm.prop('offsetHeight') + 5) + 'px';
        });

        elm.bind('click', function(event) {
          event.stopPropagation();
        });

        $document.bind('click', function(e) {
          scope.show_menu = false;
          scope.$apply();
        });
      }
    };
  });

var formatURL = function(string){
    output = string.replace('/',' ').replace('?',' ');
    return output
};

