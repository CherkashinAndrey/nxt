(function () {
  'use strict';

  angular.module('nxtlvl').filter('orderByRole', orderByRole);

  /** @ngInject */
  function orderByRole() {
    return function(items, params, state, revers) {
        var users = [];
        var admin = [];
        var constStatus = ['online','not active','offline'];
        if ( revers )  { constStatus = constStatus.reverse() };
        var resultAdmin=[];
        var resultUser=[];


        // angular.forEach(items, function(item) {
        //   if ( item.role === "admin" ) {
        //     admin.push(item);
        //   } else {
        //     users.push(item);
        //   }
        // });

        if (state == "employed") { //Ansat
           // angular.forEach(constStatus, function (el) {
           //    resultAdmin = resultAdmin.concat(admin.filter(function(user) { return user.statusAnsat == el }));
           //    resultUser = resultUser.concat(users.filter(function(user) {return user.statusAnsat == el }));
           // });
          angular.forEach(constStatus, function (el) {
              users = users.concat(items.filter(function(user) { return user.statusAnsat == el }));
          });
          return users;
        }

        if (state == "name") { 
          //   users.sort(function(a, b){
          //     return params ? a.name > b.name : a.name < b.name
          //   });
          //   admin.sort(function(a, b){
          //     return params ? a.name > b.name : a.name < b.name
          //   });
          // return admin.concat(users);
          items.sort(function(a, b){
            return revers ? a.name > b.name : a.name < b.name
          });
          return items;
        }

        if (state == "effort") { //Indsats
            angular.forEach(constStatus, function(el) {
              users = users.concat(items.filter(function(user) { return user.statusIndsats == el }));
              // resultAdmin = resultAdmin.concat(admin.filter(function(user) {return user.statusIndsats == el}));
              // resultUser = resultUser.concat(users.filter( function(user) {return user.statusIndsats == el}));
           });   
            return users;
           //   constStatus.forEach( el => {
           //    resultAdmin = resultAdmin.concat(admin.filter( (user) => user.statusIndsats == el));
           //    resultUser = resultUser.concat(users.filter( (user) => user.statusIndsats == el));
           // });        
        }

        if (state == "manager") { //Leder
          angular.forEach(constStatus, function(el) {
            users = users.concat(items.filter(function(user) { return user.statusLeder == el }));
          });
           //  angular.forEach(constStatus, function(el) {
           //    resultAdmin = resultAdmin.concat(admin.filter( function (user) {return user.statusLeder == el }));
           //    resultUser = resultUser.concat(users.filter( function (user) {return user.statusLeder == el }));
           // });
           return users;
        }
       // return resultAdmin.concat(resultUser);
       return items;
    };
  }

})();
