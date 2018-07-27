angular.module('stratusee', ['ngCookies', 'pascalprecht.translate'])
.controller('loginController', ['$scope', '$location',
    function($scope, $location) {
        var params = $location.search();

        var oeminfo = null;
        if(params.sitename) {
            oeminfo = {key: params.sitename};
        }

        $scope.oeminfo = oeminfo;
    }])