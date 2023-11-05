const validate = (event) =>{
    event.preventDefault();

    const userName = "adminUser123"
    const passWord = "lion1234"

    const usernameInput = document.getElementById("usernameInput");
    const passswordInput = document.getElementById("passwordInput");
    const incorrectUText = document.getElementById("incorrectUText");
    const incorrectPText = document.getElementById("incorrectPText");

    if(usernameInput.value !== userName){
        incorrectUText.style.visibility= "visible";
        console.log("bruhhhh 1");
        setTimeout(function () {
            incorrectUText.style.visibility = "hidden";
        }, 5000);
        return false;
    }   

    if(passswordInput.value !== passWord){
        incorrectPText.style.visibility = "visible"
        console.log("bruhhh 2");
        setTimeout(function(){
            incorrectPText.style.visibility = "hidden"
        }, 5000)
        return false;
    }

    console.log("helloo");
    location.href = "/add_courses"
}