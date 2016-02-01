(function(){
    var app = angular.module('UserApp',[])
        .config(function($interpolateProvider){
            $interpolateProvider.startSymbol('{$');
            $interpolateProvider.endSymbol('$}');
        });

    app.controller('UserController',['$scope', '$http', function($scope,$http){
        $scope.user = {
            first_name: "",
            last_name: "",
            username: "",
            email: "",
            password: "",
            retype_password: ""
        };

        $scope.error = "";

        $scope.success = false;

        $scope.submit = function(){

            $scope.error = "";
            var url = '/users/';
            $http.post(url, $scope.user)
                .success(function(data){
                    $scope.user = data;
                    $scope.success = true;
                })
                .error(function(data){
                    $scope.error = data;
                    console.log('Error to create user.');
                });
        }
    }]);
})();