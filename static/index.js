function handleSignUp(){
	alert("hello")
    email=document.getElementById("email").value
    password=document.getElementById("password").value
    data={"email":email,"password":password}
    fetch("https://abanap.herokuapp.com/sign-up",
    {
        method:"POST",
        body:JSON.stringify({"email":email,"password":password}),
        headers:{
            'Content-Type': 'application/json'
        }
    }).then(response=>response)
    .then(data=>console.log(data))
    .catch((err)=>console.log(err))
}