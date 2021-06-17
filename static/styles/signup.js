const usersignup = document.getElementById("usersignup")
usersignup.addEventListener('click', () => {
    console.log("button clicked");
    let uname = document.getElementById("name").value;
    let uemail = document.getElementById("email").value;
    let upw = document.getElementById("pw").value;
    // console.log(uname);
    // console.log(uemail);
    // console.log(upw);

})
var signupform = document.getElementById('signupform');

signupform.addEventListener("submit", handleFormSubmit);

async function handleFormSubmit() {
    var result = await getAndSubmitForm(event);
    // console.log(result);
    if (result.success) {
        
        const container = document.getElementById('container');
        container.classList.remove("right-panel-active");
    }

}

async function getAndSubmitForm(event) {
    event.preventDefault();
    const form = event.currentTarget;
    const url = "http://localhost:5000/auth/signup";
    try {
        const formData = new FormData(form);
        var data = {
            name: formData.get('name'),
            email: formData.get("email"),
            pw: formData.get('pw')
        }
        // console.log(data);
        const formDataJsonString = JSON.stringify(data);
        const fetchOptions = {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Accept": "application/json"
            },
            body: formDataJsonString,
        };
        const response = await fetch(url, fetchOptions);
        if (!response.ok) {
            const errorMessage = await response.text();
            throw new Error(errorMessage);
        }
        else {
            // console.log("login successful");
        }
        return response.json();
    } catch (error) {
        // console.error(error);
    }
}



