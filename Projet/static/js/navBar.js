    

// NAVBAR
    
    /* Set the width of the side navigation to 250px */
    /* Set the width of the side navigation to 250px and the left margin of the page content to 250px */


    let isNavOpen = false;

    
    function openNav() {
      if(isNavOpen){
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

//NAVBAR THAT OVERLAPS THE THING HERE NEXT TO THE VIDEO (YOU KNOW THE WHITE RECTANCLE WITHOUT ANY CONTENT IN IT)

let isNavOpen2 = false;
/**
 * Toggles the side navigation bar. 
 * Opens it if it's closed, and closes it if it's open.
 */
function openNav2() {
  // Display the side navigation bar
  document.getElementById("mySidenav").style.display = "block";
  document.getElementById("main").style.marginLeft = "5%";
  isNavOpen2 = true;
}

/* Close/hide the sidenav */
function closeNav2() {
  document.getElementById("mySidenav").style.display = "none";
  document.getElementById("main").style.marginLeft = "0%";
} 

// LOGIN POPUP
let isLoginScreenOpen = false;

function openLoginScreen() {

  if(isLoginScreenOpen){
      closeLoginScreen();
      isLoginScreenOpen = false;
      accessAccount();
  } else {
    // Set the height of the popup to 800px
    document.getElementById("myPopup").style.height = "600px";
    // Display the navigation bar
    document.getElementById("myPopup").style.display = "block";
    isLoginScreenOpen = true;
  }

}


function closeLoginScreen() {
  // Set the height of the popup to 0
  document.getElementById("myPopup").style.height = "0";
  // Hide the navigation bar
  document.getElementById("myPopup").style.display = "none";
  isLoginScreenOpen = false;
}

let areCommentsOpen = false;

function openComments() {

  if(areCommentsOpen){
      closeComments();
      areCommentsOpen = false;
  } else {
    // Set the height of the popup to 800px
    document.getElementById("myComments").style.height = "800px";
    // Display the navigation bar
    document.getElementById("myComments").style.display = "block";
    areCommentsOpen = true;
  }

}

function closeComments() {
  // Set the height of the popup to 0
  document.getElementById("myComments").style.height = "0";
  // Hide the navigation bar
  document.getElementById("myComments").style.display = "none";
  areCommentsOpen = false;
}