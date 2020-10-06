app.controller("casesolvingctrl", function ($scope,$http,$state,authUser) {
	
 
 $scope.CaseSolutions=[{"simiRec":{
			"SME":"No Data found",
            "confidence":"-",
		}}]	; 
	


$scope.searchCase=function(){
if($scope.pcCode=="" || $scope.pcCode==null || $scope.caseTitle=="" || $scope.caseTitle==null || $scope.caseDesc=="" ||
   $scope.caseDesc==null)
//    ||$scope.rdWS=="" || $scope.rdWS==null
//    $scope.fromDate=="" || $scope.fromDate==null||  $scope.toDate=="" || $scope.toDate==null
$scope.errorFlag= true; 
else
{
$scope.errorFlag= false;

if(authUser.getUUID()!=null)  
  $scope.UUID= authUser.getUUID();
    else
    $scope.UUID= 1;  //default

data={"uuid": $scope.UUID, "product": $scope.pcCode, "title":$scope.caseTitle, "description":$scope.caseDesc};
$http({   
    url: "Scripts/mockJson/CaseSolvingSolutions.json",
    method: "GET",
	//data: data
    }).then(function(response)                                                  
  {
   $scope.CaseSolutions= response.data.simiRecords;  
//       angular.forEach($scope.CaseSolutions,function(val){
//       var data= val.simiRec.matchedWords.split(";"); 
//       val.simiRec.matchedWords= data;
//    });
 },function(reason)
{
alert('Some error occured, please try again later!'+reason.statusText)
$state.go('login')  ;    
});		
}	
}

$scope.caseSolutionDetail=function(index)
{
   $scope.caseSolution= $scope.CaseSolutions[index].simiRec;  
}

 $( function() {
    $( "#fromDate" ).datepicker({   
        changeMonth: true,
        changeYear: true,
        dateFormat: "dd-mm-yy",
    });

  });
$( function() {
    $( "#toDate" ).datepicker({
      changeMonth: true,
      changeYear: true,
      dateFormat: "dd-mm-yy"
    });

  });


});
 



