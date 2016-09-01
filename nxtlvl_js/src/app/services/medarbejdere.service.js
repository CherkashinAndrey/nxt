(function () {
  'use strict';

  angular
    .module('nxtlvl')
    .service('MedarbejdereService', MedarbejdereService)
    .constant('URL', 'http://jsonplaceholder.typicode.com/');

  /** @ngInject */
  function MedarbejdereService($http, URL, URL_SERV, $state) {
    var service = {
      getMedarbejdere: getMedarbejdere,
      getUsers: getUsers,
      addUser: addUser,
      checkComm: checkComm,
      addUsersFile: addUsersFile,
      delUsers: delUsers,
      postAddUser: postAddUser,
      getNextGroupUser: getNextGroupUser,
      getUsersGet: getUsersGet,
      getManagers:getManagers
    };

    return service;

    function postAddUser(user, dom) {
        console.log("postAddUser",user);
        $http({
          method: 'POST',
          url: URL_SERV +  "/employee" + '/add'+ "/",
          data: user
        })
        .then(
          function (result) {
            console.log(result);
            $state.go('home.medarbejdere');
          },
          function (error) {
            console.log(error); 
            dom.removeClass("ng-hide ")
            dom.addClass(" ng-show")
          }
        )
    }

    function getManagers() {
      return $http({
                    method: 'GET',
                    url: URL_SERV + "/employee" + '/manager/',
                    xhrFields: {
                      withCredentials: true
                    }
                  });
    }

    function getUsersGet(idUser) {
        console.log(URL_SERV + "/employee" + '/json_id' + '/' + idUser + "/");
      return $http({
                    method: 'GET',
                    url: URL_SERV + "/employee" + '/json_id' + '/' + idUser + "/",
                    xhrFields: {
                      withCredentials: true
                    }
                  });
    }

    function getMedarbejdere() {
   //   return medarbejdere;
    }

    function getUsers() {
      //return medarbejdereUser;
    }

    function checkComm(index) {
      medarbejdereUser.map( function (el) { 
        if (el.id == index) {
          el.checkComm = !el.checkComm;
        }
      });
     // medarbejdereUser[index].checkComm = !medarbejdereUser[index].checkComm;
    }

    function addUsersFile(file, idCompany, dom) {
      console.log(URL_SERV + '/add_many_employee/' + idCompany, "file:", file, "idCompany:",idCompany);
     dom.addClass('loading');
      // scope.MedarbejdereAnsatController.loadState = 1;
        return $http({
          method: 'POST',
          url: URL_SERV + '/add_many_employee/' + idCompany + "/",
          data: file
        })
        .then(
          function (result) {
            console.log('result',result);
            // setTimeout(function() { 
              dom.removeClass('loading');
              dom.addClass('loaded');
            //   // scope.MedarbejdereAnsatController.loadState = 2;
            //   console.log('result',result)
            //   return result;
            // }, 3000);
          },
          function (error) {
            dom.removeClass('loading');
            dom.removeClass('loaded');
            dom.addClass('error');
            // scope.MedarbejdereAnsatController.loadState = 3; // error
            console.log(error); 
          }
        )
      }

    function addUser(user) {
      medarbejdereUser.push(user);
    }

    function delUsers () {
      return medarbejdereUser = [];
    }

    function getNextGroupUser (user) {
      return  groupNextUser;

    }
    // var medarbejdere = [
    //   {
    //     model: true,
    //     name: 'Navn Navnsesen (Niv 1.)',
    //     type: 'Classic',
    //     guide: {
    //       link: 'udfyld',
    //       img: 'udfyld',
    //       complete: false,
    //       text: 'Ikke afsluttet'
    //     },
    //     leaders: {
    //       link: 'PDF',
    //       img: 'pdf',
    //       complete: false,
    //       text: 'Ikke afsluttet'
    //     },
    //     options: {
    //       text: 'Fjern',
    //       options: 'delete'
    //     },
    //     insert: {
    //       text: 'udfyld',
    //       complete: false
    //     },
    //     medarbejdere: [
    //       {
    //         model: false,
    //         name: 'Navn Navnsesen (Niv 2.)',
    //         type: 'Classic',
    //         guide: {
    //           link: '',
    //           img: 'eye',
    //           complete: true,
    //           text: 'Ikke afsluttet'
    //         },
    //         leaders: {
    //           complete: true,
    //           text: 'Ikke afsluttet'
    //         },
    //         options: {
    //           text: 'Fjern',
    //           options: 'delete'
    //         },
    //         insert: {
    //           text: 'udfyld',
    //           complete: true
    //         },
    //         medarbejdere: [
    //           {
    //             model: false,
    //             name: 'Navn Navnsesen (Niv 3.)',
    //             type: 'Classic',
    //             guide: {
    //               link: 'PDF',
    //               img: 'pdf',
    //               complete: true,
    //               text: 'Ikke afsluttet'
    //             },
    //             leaders: {
    //               complete: false,
    //               text: 'Ikke afsluttet'
    //             },
    //             options: {
    //               text: 'Fjern',
    //               options: 'delete'
    //             },
    //             insert: {
    //               text: 'udfyld',
    //               complete: true
    //             },
    //             medarbejdere: [

    //             ]
    //           }
    //         ]
    //       },
    //       {
    //         model: false,
    //         name: 'Navn Navnsesen (Niv 2.)',
    //         type: 'Classic',
    //         guide: {
    //           link: 'udfyld',
    //           img: 'udfyld',
    //           complete: false,
    //           text: 'Ikke afsluttet'
    //         },
    //         leaders: {
    //           link: 'PDF',
    //           img: 'pdf',
    //           complete: false,
    //           text: 'Ikke afsluttet'
    //         },
    //         options: {
    //           text: 'Fjern',
    //           options: 'delete'
    //         },
    //         insert: {
    //           text: 'udfyld',
    //           complete: false
    //         },
    //         medarbejdere: []
    //       }
    //     ]
    //   },
    //   {
    //     model: true,
    //     name: 'Navn Navnsesen (Niv 1.)',
    //     type: 'Classic',
    //     guide: {
    //       link: 'udfyld',
    //       img: 'udfyld',
    //       complete: true,
    //       text: 'Ikke afsluttet'
    //     },
    //     leaders: {
    //       complete: false,
    //       text: 'Ikke afsluttet'
    //     },
    //     options: {
    //       text: 'Fjern',
    //       options: 'delete'
    //     },
    //     insert: {
    //       text: 'udfyld',
    //       complete: false
    //     },
    //     medarbejdere: [
    //       {
    //         model: false,
    //         name: 'Navn Navnsesen (Niv 2.)',
    //         type: 'Classic',
    //         guide: {
    //           link: 'udfyld',
    //           img: 'udfyld',
    //           complete: true,
    //           text: 'Ikke afsluttet'
    //         },
    //         leaders: {
    //           complete: true,
    //           text: 'Ikke afsluttet'
    //         },
    //         options: {
    //           text: 'Fjern',
    //           options: 'delete'
    //         },
    //         insert: {
    //           text: 'udfyld',
    //           complete: false
    //         },
    //         medarbejdere: []
    //       }
    //     ]
    //   }
    // ];

    // var medarbejdereUser = [
    
    // {
    //   id: 4123,
    //   login: 'nt',
    //   name: 'Jane Hahn',
    //   lastName: 'Hahn',
    //   manager: 'Name 1',
    //   title: 'Partner/cand.comm. & BA scient.pol. Virksomhedsrådgiver & certificeret coach',
    //   email: 'admin@chi.com',
    //   mobile: '(+3) 8 050 4567832',
    //   company: 'NXT LVL',
    //   role: 'admin',
    //   ownLeader: 'Navn Navnesen',
    //   type: 'Classic A',
    //   firstDate: '20. Nov. 2001',
    //   middleDate: '25. Nov. 2001',
    //   lastDate: '20. Nov. 2002',
    //   status: '??????',
    //   statusAnsat: 'online',
    //   statusIndsats: 'online',
    //   statusLeder: 'online',
    //   isManager: true,
    //   potencial: 'Ja',
    //   checkComm: false,
    //   note: 'Kunne have potentiale indenfor salg. Vi må holde fast på denne medarbejder, og råder til at lorem ipsum dolor.'
    // },
    // {
    //   id: 124,
    //   login: 'man1',
    //   name: 'Franz Malten Buemann',
    //   lastName: 'Buemann',
    //   manager: 'Name 1',
    //   title: 'Partner/cand.comm. & BA scient.pol. Virksomhedsrådgiver & certificeret coach',
    //   email: 'user@chi.com',
    //   mobile: '(+3) 8 095 1111111',
    //   company: 'NXT LVL',
    //   role: 'user',
    //   ownLeader: 'Navn Navnesen',
    //   type: 'Classic B',
    //   firstDate: '20. Nov. 2001',
    //   middleDate: '25. Nov. 2001',
    //   lastDate: '20. Nov. 2002',
    //    status: '??????',
    //   statusAnsat: 'not active',
    //   statusIndsats: 'online',
    //   statusLeder: 'offline',
    //   isManager: false,
    //   potencial: 'Ja',
    //   checkComm: false,
    //   note: 'Kunne have potentiale indenfor salg. Vi må holde fast på denne medarbejder, og råder til at lorem ipsum dolor.'
    // }
    // ];

    // var groupNextUser= [{
    //   id: 12,
    //   login: 'man1',
    //   name: '12',
    //   lastName: '12',
    //   manager: 'Name 1',
    //   title: 'Partner/cand.',
    //   email: 'user12@chi.com',
    //   mobile: '(+3) 8 095 1111111',
    //   company: 'NXT LVL',
    //   role: 'user',
    //   ownLeader: 'Navn Navnesen',
    //   type: 'Classic B',
    //   firstDate: '20. Nov. 2001',
    //   middleDate: '25. Nov. 2001',
    //   lastDate: '20. Nov. 2002',
    //    status: '??????',
    //   statusAnsat: 'not active',
    //   statusIndsats: 'online',
    //   statusLeder: 'offline',
    //   isManager: true,
    //   potencial: 'Ja',
    //   checkComm: false,
    //   note: 'Kunne have potentiale indenfor salg. Vi må holde fast på denne medarbejder, og råder til at lorem ipsum dolor.'
    // },
    // {
    //   id: 13,
    //   login: 'man1',
    //   name: '13',
    //   lastName: '13',
    //   manager: 'Name 1',
    //   title: 'certificeret coach',
    //   email: 'user13@chi.com',
    //   mobile: '(+3) 8 095 1111111',
    //   company: 'NXT LVL',
    //   role: 'user',
    //   ownLeader: 'Navn Navnesen',
    //   type: 'Classic B',
    //   firstDate: '20. Nov. 2001',
    //   middleDate: '25. Nov. 2001',
    //   lastDate: '20. Nov. 2002',
    //    status: '??????',
    //   statusAnsat: 'not active',
    //   statusIndsats: 'online',
    //   statusLeder: 'offline',
    //   isManager: false,
    //   potencial: 'Ja',
    //   checkComm: false,
    //   note: 'Kunne have potentiale indenfor salg. Vi må holde fast på denne medarbejder, og råder til at lorem ipsum dolor.'
    // }];

    // var groupNextUser2= [{
    //   id: 666,
    //   login: 'man1',
    //   name: '666',
    //   lastName: '666',
    //   manager: 'Name 1',
    //   title: 'Partner/cand.',
    //   email: 'user12@chi.com',
    //   mobile: '(+3) 8 095 1111111',
    //   company: 'NXT LVL',
    //   role: 'user',
    //   ownLeader: 'Navn Navnesen',
    //   type: 'Classic B',
    //   firstDate: '20. Nov. 2001',
    //   middleDate: '25. Nov. 2001',
    //   lastDate: '20. Nov. 2002',
    //    status: '??????',
    //   statusAnsat: 'not active',
    //   statusIndsats: 'online',
    //   statusLeder: 'offline',
    //   isManager: false,
    //   potencial: 'Ja',
    //   checkComm: false,
    //   note: 'Kunne have potentiale indenfor salg. Vi må holde fast på denne medarbejder, og råder til at lorem ipsum dolor.'
    // },
    // {
    //   id: 222,
    //   login: 'man1',
    //   name: '2222',
    //   lastName: '222',
    //   manager: 'Name 1',
    //   title: 'certificeret coach',
    //   email: 'user13@chi.com',
    //   mobile: '(+3) 8 095 1111111',
    //   company: 'NXT LVL',
    //   role: 'user',
    //   ownLeader: 'Navn Navnesen',
    //   type: 'Classic B',
    //   firstDate: '20. Nov. 2001',
    //   middleDate: '25. Nov. 2001',
    //   lastDate: '20. Nov. 2002',
    //    status: '??????',
    //   statusAnsat: 'not active',
    //   statusIndsats: 'online',
    //   statusLeder: 'offline',
    //   isManager: false,
    //   potencial: 'Ja',
    //   checkComm: false,
    //   note: 'Kunne have potentiale indenfor salg. Vi må holde fast på denne medarbejder, og råder til at lorem ipsum dolor.'
    // }];


  }

})();
