app.controller("loginctrl", function ($scope,$state,$http) {
    $scope.msg = "Login Screen";
    $scope.usr = "john"; //empty value afterwards
    $scope.pwd = "john123";  //empty value afterwards
    $scope.errorMsg=false;
    $scope.errorMessageText="Invalid Credentials !!! Please try again";
//    $scope.errorMessageText="Some error occured!";
    $scope.keyUpLogin=function(event){ 
      if(event.keyCode == 13){
        $("#login").click();
    }  
}
$scope.loginpage=function(){
data = {
username: $scope.usr, 
password: $scope.pwd
};
if($scope.usr==null || $scope.pwd==null || $scope.usr=="" || $scope.pwd=="")    
{ 
$scope.errorMsg=true;
if($scope.usr==null || $scope.usr=="") 
$scope.errorMessageText="Please enter a valid username";  
else if($scope.pwd==null || $scope.pwd=="") 
$scope.errorMessageText="Please enter a valid password";       
}
else   
{

 $http({
    url: "Scripts/mockJson/credentials.json", 
    method: "GET",
    //data:JSON.stringify(data)	
    }).then(function(response){ 
	
	User=$scope.usr;
//	UUID= response.data.uuid;
	UUID= 1;
	
      if($scope.usr==response.data.username && $scope.pwd==response.data.password)
    {   
        $scope.errorMsg=false;
        $state.go('nokiamain');
    }
  
    else{
        $scope.errorMsg=true;
//        $scope.errorMessageText=response.data.message;
        $scope.usr=$scope.pwd="";
    }       
},function(reason){  
    alert('Some error occured, please try again later!'+reason.statusText)
    $scope.usr=$scope.pwd="";
     console.log($scope.usr);
    $state.go('login');      
});  
    
}
}


 }).factory('authUser', function(){    //Service for getting username
    
    var getUser_Name = function(){
            if(!("undefined" === typeof User))
          return User;
          else
          return null ;
  };  
    var getUUID = function(){
            if(!("undefined" === typeof UUID))
          return UUID;
          else
          return null ;
  };  
    return {    
    getUser_Name:getUser_Name,
	getUUID:getUUID
  };
}); 