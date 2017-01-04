(function(){
    var app = angular.module('UserApp', [])
        .config(function($interpolateProvider){
            $interpolateProvider.startSymbol('{$');
            $interpolateProvider.endSymbol('$}');
        });

    app.factory('fbAuth', function($rootScope, $http){
        return {
            watchLoginChange: function() {

                var _self = this;

                this.getUserInfo = function(){
                    FB.api('/me', function(res) {
                        $rootScope.$apply(function() {
                            $rootScope.fbuser = res;
                        });
                    });
                };

                this.getToken = function(authResponse){
                    $http.post(url_fb_token, {accessToken: authResponse.accessToken })
                        .success(function(data){
                            console.log(data);
                        })
                        .error(function(data){
                            console.log("Error: token wasn't taken!");
                        });
                };

                FB.Event.subscribe('auth.authResponseChange', function(res) {
                    if (res.status === 'connected') {
                        console.log("logged!!!!!!!!!!!!!");
                        _self.getUserInfo();
                        _self.getToken(res.authResponse);
                    }
                    else {
                        console.log("not logged!!!!!!!!!!!!!");
                    }

                });

            }
        }
    });

    app.run(['$rootScope', '$window', 'fbAuth', function($rootScope, $window, fbAuth) {

        $rootScope.fbuser = {};

        $window.fbAsyncInit = function() {

            FB.init({
                appId      : '1071687446243206',
                xfbml      : true,
                version    : 'v2.8'
            });

            fbAuth.watchLoginChange();
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

    app.controller('UserCtrl', ['$scope', '$http', '$window', 'fbAuth', function ($scope, $http, $window, fbAuth) {
        $scope.user = {username: '', password: '', name: ''};
        $scope.message = '';
        $scope.next = url_next;

        if($window.sessionStorage.token != null){
            $http.get(url_authetication_me)
                .success(function(data){
                    console.log(data);
                    $scope.user.name = data.first_name;
                })
                .error(function(data){
                    console.log(data);
                });
        }

        $scope.testOut = function(){
            console.log("what?");
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

        $scope.logout = function(){
            if($window.sessionStorage.token != null){
                delete $window.sessionStorage.token;
                $window.location = url_authetication_index;
            }
        };

        $scope.isAutheticated = function(){
            return $window.sessionStorage.token != null;
        };
    }]);
})();