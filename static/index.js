	
        document.addEventListener('DOMContentLoaded', () => {
  
            loginForm = document.getElementById('userform');

            if (localStorage.getItem("username") != null) {
                const username = localStorage.getItem("username");
                console.log( "username in localStorage:", username);
                loginForm.username.value = username;
            }


            loginForm.addEventListener('submit', event => {
                event.preventDefault();
                let username = loginForm.username.value;
                localStorage.setItem("username", username);      
                loginForm.submit();

                document.querySelector("#tester").innerHTML = username;
            });

        });