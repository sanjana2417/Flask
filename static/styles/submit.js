const submitbtn = document.getElementById("submit")
function submit(doc) {
    const fetchOptions = {
        method: "POST",
        headers: {
            "Content-type": "application/json; charset=UTF-8"
        },
        body: doc,
    };

    const response = fetch('http://localhost:5000/submitblog', fetchOptions);

    return response;
}
submitbtn.addEventListener('click', () => {
    console.log("button clicked");
    let title = document.getElementById("blogtitle").value;
    let content = document.getElementById("content").value;
    let uname = document.getElementById("uname").value;
    // console.log(title);
    // console.log(content);
    var doc = {
        title: title,
        content: content,
        uname: uname
    }
    doc = JSON.stringify(doc)
    const result = submit(doc)
    // console.log(result)
    // to check i working
    // if (result) {
    //     console.log("true");
    // }
    // else {
    //     console.log("false");
    // }

})