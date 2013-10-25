'use strict';

var Listen = angular.module('Listen',[], function($interpolateProvider) {
    $interpolateProvider.startSymbol('[[');
    $interpolateProvider.endSymbol(']]')
});

Listen.controller('signupCtrl', function($scope, $http) {

    $scope.signupResponse = "";

    $scope.signupUser = function() {
        $http.post($scope.signupUrl,
                   {
                       'signupEmail': $scope.signupEmail
                   }).success(function(data) {
                       $scope.signupResponse = data
                   }).error(function(data) {
                       console.log("Sorry, can't register!");
                   });
    }

});


Listen.controller('loginCtrl', function($scope, $http) {

    $scope.loginUser = function() {
        $http.post($scope.loginUrl,
                   {
                       'loginEmail': $scope.loginEmail,
                       'loginPassword': $scope.loginPassword
                   }).success(function(data) {
                       window.location = data;
                   }).error(function(data) {
                       console.log("Sorry can't login");
                   });
    }

});


Listen.controller('createAccountCtrl', function($scope, $http) {

    $scope.passwordVerify = "";

    $scope.comparePasswords = function() {
        if($scope.loginPassword == $scope.loginPasswordVerify) {
            $scope.passwordVerify = "Cool.";
            return true;
        } else {
            $scope.passwordVerify = "Passwords Don't Match";
            return false;
        }
    }

    $scope.createAccount = function() {

        if($scope.comparePasswords()) {

            $http.post($scope.createAccountUrl,
                       {
                           'accountUsername': $scope.loginEmail,
                           'accountPassword': $scope.loginPassword,
                           'accountEmail': $scope.accountEmail,
                           'signupToken': $scope.signupToken
                       }).success(function(data) {
                           window.location = data;
                       }).error(function(data) {
                           console.log("Sorry can't login");
                       });
        }


    }
});






