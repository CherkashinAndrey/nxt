(function() {
  'use strict';

  angular
    .module('nxtlvl')
    .config(routerConfig);

  /** @ngInject */
  function routerConfig($stateProvider,$locationProvider, $urlRouterProvider, ADMINS, USERS) {
    $stateProvider
      // .state('/', {
      //   url: '/',
      //   templateUrl: 'app/choose/choose-user.html',
      //   controller: 'ChooseUserController',
      //   controllerAs: 'chooseCtrl'
      // })
      .state('home', {
        url: '/home',
        templateUrl: 'app/main/main.html',
        controller: 'MainController',
        controllerAs: 'mainCtrl'
      })
      .state('home.velkommen', {
        url: '/velkommen',
        data: {
          roles: USERS
        },
        templateUrl: 'app/velkommen/velkommen.html',
        controller: 'VelkommenController',
        controllerAs: 'velkommenCtrl'
      })
      .state('home.forberedelsen', {
        url: '/forberedelsen',
        data: {
          roles: ADMINS
        },
        templateUrl: 'app/forberedelsen/forberedelsen.html',
        controller: 'ForberedelsenController',
        controllerAs: 'forberedelsenFirstCtrl'
      })
      .state('home.forberedelsen-start', {
        url: '/forberedelsen-start',
        data: {
          roles: ADMINS
        },
        templateUrl: 'app/forberedelsen/forberedelsen.start.html',
        controller: 'ForberedelsenStartController',
        controllerAs: 'forberedelsenCtrl'
      })
      .state('home.samtalen', {
        url: '/samtalen',
        data: {
          roles: ADMINS
        },
        templateUrl: 'app/samtalen/samtalen.html'
      })
      .state('home.indsatsen', {
        url: '/indsatsen',
        data: {
          roles: ADMINS
        },
        templateUrl: 'app/indsatsen/indsatsen.html',
        controller: 'IndsatsenController',
        controllerAs: 'indsatsenCtrl'
      })
      .state('home.medarbejdere', {
        url: '/medarbejdere',
        data: {
          roles: ADMINS
        },
        templateUrl: 'app/medarbejdere/medarbejdere.html',
        controller: 'MedarbejdereController',
        controllerAs: 'medarbejdereCtrl'
      })
      .state('home.profile', {
        url: '/profile',
        data: {
          roles: USERS
        },
        templateUrl: 'app/profile/profile.html',
        controller: 'ProfileController',
        controllerAs: 'profileCtrl'
      })
      .state('home.tilfotAnsat', {
        url: '/medarbejdere/ansat',
        data: {
          roles: ADMINS
        },
        templateUrl: 'app/medarbejdere/tilfoj/medarbejdereAnsat.html',
        controller: 'MedarbejdereAnsatController',
        controllerAs: 'MedarbejdereAnsatCtrl'
      })
      .state('home.tilfotForberedelsen', {
        url: '/medarbejdere/forberedelsen',
        data: {
          roles: ADMINS
        },
        templateUrl: 'app/medarbejdere/tilfoj/medarbejdereForberedelsen.html',
        controller: 'MedarbejdereForberedelsenController',
        controllerAs: 'MedarbejdereForberedelsenCtrl',
        params: {
            user: null,
        }
      })
      .state('login', {
        url: '/login',
        templateUrl: 'app/login/login.html',
        controller: 'LoginController',
        controllerAs: 'Login'
      })
      .state('home.editProfile', {
        url: '/editProfile',
        data: {
          roles: ADMINS
        },
        templateUrl: 'app/profile/editProfile.html',
        controller: 'EditProfileController',
        controllerAs: 'profileCtrl',
        params: {
            user: null,
            currentUserRole: null
        }
      });
    $locationProvider.html5Mode(true);
    $urlRouterProvider.otherwise('/login');
  }

})();
