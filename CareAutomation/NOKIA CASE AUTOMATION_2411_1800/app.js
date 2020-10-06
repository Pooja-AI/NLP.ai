var app = angular.module("myApp", ['ui.router']);
app.config(function($stateProvider,$urlRouterProvider) {
    $stateProvider
	
	.state('index', {
        url: '/index',
        templateUrl : "index.html",
        controller  : "indexctrl"
	})
	
    .state('login', {
        url: '/login',
        templateUrl : "login.html",
        controller  : "loginctrl"
	})
	
	.state("nokiamain", {
        url : "/nokiamain",
        templateUrl : "nokiamain.html",       
        controller : "nokiamainctrl"
    })
	
	.state("nokiamain.carecase", {
         url : "/carecase",
        templateUrl : "carecase.html",       
        controller : "carecasectrl"
    })
	
	.state("nokiamain.similarcases", {
         url : "/similarcases",
        templateUrl : "similarcases.html",       
        controller : "similarcasesctrl"
    })
	
	.state("nokiamain.casesolving", {
         url : "/casesolving",
        templateUrl : "casesolving.html",       
        controller : "casesolvingctrl"
    })
	
	.state("nokiamain.loganalysis", {
         url : "/loganalysis",
        templateUrl : "loganalysis.html",       
        controller : "loganalysisctrl"
    })
    .state("nokiamain.help", {
         url : "/help",
        templateUrl : "help.html",       
        controller : "helpctrl"
    })
	
    $urlRouterProvider.otherwise("/login");
});

