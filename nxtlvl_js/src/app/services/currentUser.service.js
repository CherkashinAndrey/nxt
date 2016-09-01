(function () {
  'use strict';

  angular.module('nxtlvl').service('currentUserService', currentUserService);

  /** @ngInject */
  function currentUserService($http, URL_SERV) {
    var currentUser= {
    }

    var service = {
      saveUser: saveUser,
      getCurrentUser: getCurrentUser,
      overwriteUser: overwriteUser,
      postEditProfile: postEditProfile,
      postPhoto: postPhoto,
    //  getPhoto: getPhoto
    };

    return service;

    function saveUser(user) {
      currentUser = user;
    }

    function getCurrentUser(id) {
      return $http({
                    method: 'GET',
                    url: URL_SERV + "/profile" + '/show' + '/' + id,
                    xhrFields: {
                      withCredentials: true
                    }
                    });
    }

    function overwriteUser(oldUser) {
      currentUser = oldUser;
    }

    function postEditProfile (editUser, idUser) {
      return $http({
              method: 'POST',
              url: URL_SERV + "/employee/update/" + idUser + "/",
              xhrFields: {
                      withCredentials: true
                    },
              data: editUser
            })
            // .then(
            // function (result) {
            //    console.log("EDIT",result); 
            // },
            // function (error) {
            //   console.log("EDIT",error); 
            // });
    }

    function postPhoto (idUser, photo) {
        return $http({
          method: 'POST',
          url: URL_SERV + "/upload_photo/" + idUser + "/",
          xhrFields: {
                  withCredentials: true
                },
          data: photo
        })
    }

    // function getPhoto (idUser) {
    //     return $http({
    //       method: 'GET',
    //       url: URL_SERV + "/upload_photo/" + idUser + "/",
    //       xhrFields: {
    //               withCredentials: true
    //             }
    //     })
    // }


  }
})();
