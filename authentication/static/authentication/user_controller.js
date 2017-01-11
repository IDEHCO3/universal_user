(function(){
    var app = angular.module('UserApp', [])
        .config(function($interpolateProvider){
            $interpolateProvider.startSymbol('{$');
            $interpolateProvider.endSymbol('$}');
        });

    app.factory('fbAuth', function($rootScope, $http, $window){
        var that = this;
        this.getToken = function(authResponse){
            $http.post(url_fb_token, {accessToken: authResponse.accessToken })
                .success(function(data){
                    $window.sessionStorage.token = data['token'];
                    $window.location.reload();
                })
                .error(function(data){
                    console.log("Error: token wasn't taken!");
                });
        };

        this.setToken = function(response){
            if (response.status === 'connected') {
                console.log("logged!!!!!!!!!!!!!");
                that.getToken(response.authResponse);
            }
            else {
                console.log("not logged!!!!!!!!!!!!!");
                if($window.sessionStorage.token != null) {
                    delete $window.sessionStorage.token;
                }
            }
        };

        return {
            loadToken: function(){
                if ($window.sessionStorage.token == null) {
                    FB.getLoginStatus(function (response) {
                        that.setToken(response);
                    });
                }
            },
            watchLoginChange: function() {

                FB.Event.subscribe('auth.authResponseChange', function(response) {
                    that.setToken(response);
                });

            },
            logout: function(){
                FB.getLoginStatus(function(response) {
                    if (response && response.status === 'connected') {
                        FB.logout(function(response) {
                            FB.Auth.setAuthResponse(null, 'unknown');
                            console.log("logged out",response);
                            $window.location.reload();
                        });
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

            fbAuth.loadToken();
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

        $scope.logout = function(){
            if($window.sessionStorage.token != null){
                delete $window.sessionStorage.token;
                $scope.user = {username: '', password: '', name: ''};
                $scope.message = '';
                fbAuth.logout();
                $window.location.reload();
            }
        };

        $scope.isAutheticated = function(){
            return $window.sessionStorage.token != null && $scope.user.name != '';
        };

        $scope.loadUserData();
    }]);
})();