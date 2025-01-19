    /* Set the width of the side navigation to 250px */
    /* Set the width of the side navigation to 250px and the left margin of the page content to 250px */

    let isNavOpen = false;
    function openNav() {
      if(isNavOpen){
        console.log("close");
          closeNav();
          isNavOpen = false;
      } else {
        document.getElementById("mySidenav").style.width = "14%";
        document.getElementById("main").style.marginLeft = "14%";
        isNavOpen = true;
      }
      
    }
    
    /* Set the width of the side navigation to 0 and the left margin of the page content to 0 */
    function closeNav() {
      document.getElementById("mySidenav").style.width = "0%";
      document.getElementById("main").style.marginLeft = "0%";
      isNavOpen = false;
    }
    