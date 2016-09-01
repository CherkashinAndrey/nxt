(function () {
  'use strict';

  angular
    .module('nxtlvl')
    .service('LoginService', LoginService)
    .constant('URL_LOCAL', 'http://127.0.0.1:8000/login')
    .constant('URL_LOGIN', 'http://192.168.2.105:8000/login')
    .constant('URL_SHOW', 'http://192.168.2.232:8000/employee/show');

  /** @ngInject */
  function LoginService($http, URL_LOCAL, URL_LOGIN, URL_SERV, URL_SHOW, UserService, $state, $localStorage, currentUserService, MedarbejdereService, $cookies) {
    
    var service = {
      userLogin: userLogin,
      postLogin: postLogin,
      postLoginReset:postLoginReset,
      logOut:logOut
    };

    return service;

    function userLogin(login, dom) {
     // debugger
        // if (login.email == 'admin@chi.com') {
        //   var users = MedarbejdereService.getUsers();
        //   var user = users.filter( function(item) {
        //     return item.email == login.email
        //   });

        //   currentUserService.saveUser(user[0]);
        //   UserService.chooseRole(user[0].role);
        //   $localStorage['users'] = user[0];
        //   $state.go('home.medarbejdere');
        //   MedarbejdereService.delUsers(); //dellete
        //   return user;
        // }

        // if (login.email == 'user@chi.com') {
        //   var users = MedarbejdereService.getUsers();
        //   var user = users.filter( function(item) {
        //     return item.email == login.email
        //   });
        //   currentUserService.saveUser(user[0]);
        //   $localStorage['users'] = user[0];
        //   UserService.chooseRole(user[0].role);
        //   $state.go('home.velkommen');
        //   MedarbejdereService.delUsers();  //dellete
        //   return user;
        // }else {
        //   dom.addClass('form-error');
        // }

    }

    function postLoginReset(email) {
      console.log(email);
      return $http({
          method: 'POST',
          url: URL_SERV + "/password_reset/",
          data: email
        })
        .then(
          function (result) {
            console.log("logout",result)
        },
        function (error) {
          console.log('error:',error);
        })
    }

    function logOut() {
      return $http({
          method: 'POST',
          url: URL_SERV + "/logout/",
          data: {}
        })
        .then(
          function (result) {
            console.log("logout",result)
        },
        function (error) {
          console.log('error:',error);
        })
    }

    function postLogin(login) {
      var manager;
     // console.log( location.protocol + "//"+ location.host + "/login");
      console.log(login);
        return $http({
          method: 'POST',
          url: URL_SERV + "/login",
          data: login
        })
        .then(
          function (result) {
            // console.log($cookies.getAll()); 
            // console.log($cookies.getAll().csrftoken);
            console.log("Login",result.data);
            $localStorage['users'] = result.data;
            // email            :            "rfg@gmail.com"
            // employee_id      :            1
            // user_id          :            3
            return  $http({
                    method: 'GET',
                    url: URL_SERV + '/profile/show' + '/' + result.data.employee_id + "/",
                    xhrFields: {
                      withCredentials: true
                    }
                    }) 

          })
        .then(
          function (result) {
           // $localStorage['users'] = result.data;
            //debugger
          //  debugger
           var managerName = Object.assign(result.data, {first_name: result.data.user.split(' ')[0], last_name:result.data.user.split(' ').splice(1).join(' ')});
            $localStorage['usersManager'] = managerName;
            // console.log('resultGET!!!',result.data);
            $state.go('home.profile');
          }
        ),
        // .then(
        //         function (result) {
        //           console.log(result);
        //           // UserService.chooseRole('Leder'); // Muligheder
        //           // currentUserService.saveUser();
        //           // $localStorage['users'] = result.data;
        //           // UserService.chooseRole(result.role);
        //           // $localStorage['users'] = {'role':'Leder','token':'adafgasdgsdfgsdfgbsgfytnilikjuh'};
        //           // $state.go('home.medarbejdere');
        //           // console.log('result',result);
        //           // console.log('$localStorage',$localStorage);
        //           return result;
        //         }),
        function (error) {
          console.log('error:',error);
        }
    }

  }

})();
