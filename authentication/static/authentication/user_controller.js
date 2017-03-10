(function(){
    var app = angular.module('UserApp', [])
        .config(function($interpolateProvider){
            $interpolateProvider.startSymbol('{$');
            $interpolateProvider.endSymbol('$}');
        });


    app.run(['$rootScope', '$window', function($rootScope, $window) {

        $window.fbAsyncInit = function() {
            FB.init({
                appId      : '1071687446243206',
                xfbml      : true,
                version    : 'v2.8'
            });
        };

        (function(d){
            var js,
            id = 'facebook-jssdk',
            ref = d.getElementsByTagName('script')[0];
            if (d.getElementById(id)) {return;}
            js = d.createElement('script');
            js.id = id;
            js.async = true;
            js.src = "//connect.facebook.net/en_US/sdk.js";
            ref.parentNode.insertBefore(js, ref);
        }(document));
    }]);

    app.factory('authInterceptor', function ($rootScope, $q, $window) {
        return {
            request: function (config) {
                config.headers = config.headers || {};
                if ($window.sessionStorage.token) {
                    config.headers.Authorization = 'JWT ' + $window.sessionStorage.token;
                }
                return config;
            },
            response: function (response) {
                if (response.status === 401) {
                // handle the case where the user is not authenticated
                }
                return response || $q.when(response);
            }
        };
    });

    app.config(function ($httpProvider) {
        $httpProvider.interceptors.push('authInterceptor');
    });

    app.controller('UserCtrl', ['$scope', '$http', '$window', function ($scope, $http, $window) {
        $scope.user = {username: '', password: '', name: ''};
        $scope.message = '';
        $scope.next = url_next;

        var that = this;

        this.getToken = function(authResponse){
            $http.post(url_fb_token, {accessToken: authResponse.accessToken, userID: authResponse.userID })
                .success(function(data){
                    $window.sessionStorage.token = data['token'];
                    $window.location = $scope.next;
                })
                .error(function(data){
                    console.log("Error: token wasn't taken!");
                });
        };

        $scope.loadUserData = function() {
            if ($window.sessionStorage.token != null) {
                $http.get(url_authetication_me)
                    .success(function (data) {
                        console.log(data);
                        $scope.user.name = data.first_name;
                    })
                    .error(function (data) {
                        console.log(data);
                        delete $window.sessionStorage.token;
                        $window.location.reload();
                    });
            }
        };

        $scope.submit = function () {
            $http.post(url_authetication_token, $scope.user)
                .success(function (data, status, headers, config) {
                    $window.sessionStorage.token = data.token;
                    $scope.message = 'Welcome';
                    $window.location = $scope.next;
                    console.log(data);
                })
                .error(function (data, status, headers, config) {
                    // Erase the token if the user fails to log in
                    delete $window.sessionStorage.token;
                    console.log(data);

                    // Handle login errors here
                    $scope.message = 'Error: Invalid user or password';
                });
        };

        $scope.loginFacebook = function(){
            FB.login(function(response){
                if (response.status === 'connected') {
                    console.log("logged on facebook!");
                    that.getToken(response.authResponse);
                }
                else {
                    console.log("Not logged on facebook!");
                }
            },{
                scope: 'email',
                return_scopes: true
            });
        };

        $scope.logout = function(){
            if($window.sessionStorage.token != null){
                delete $window.sessionStorage.token;
                $scope.user = {username: '', password: '', name: ''};
                $scope.message = '';
                $window.location.reload();
            }
        };

        $scope.isAutheticated = function(){
            return $window.sessionStorage.token != null && $scope.user.name != '';
        };

        $scope.loadUserData();
    }]);
})();