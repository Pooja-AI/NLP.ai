app.controller('nokiamainctrl', function ($scope,$state,$http,authUser) {

if(authUser.getUser_Name()!=null)  
  $scope.user_name= authUser.getUser_Name();
    else
    $scope.user_name= "User"; 


var dNow = new Date();
var localdate= dNow.getDate() + '/' + (dNow.getMonth()+1) + '/' + dNow.getFullYear() + ' ' + dNow.getHours() + ':' + dNow.getMinutes();
$scope.currentDate= localdate;

$state.go('nokiamain.carecase');
		
	$scope.logOut= function(){
		$state.go('login');		
	}	
});
