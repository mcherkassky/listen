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

var formatURL = function(string){
    output = string.replace('/',' ').replace('?',' ');
    return output
};