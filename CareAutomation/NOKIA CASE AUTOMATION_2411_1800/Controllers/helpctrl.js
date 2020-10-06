app.controller('helpctrl', function ($scope,$location,$anchorScroll) {

 $scope.gotohelp = function(x) {
      var newHash = 'help' + x;
      if ($location.hash() !== newHash) 
        $location.hash('help' + x);
       else
        $anchorScroll();
      }      
    
});

