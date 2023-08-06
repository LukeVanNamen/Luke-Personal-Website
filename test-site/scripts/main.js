async function getNumVisitors() {
    try {
        await fetch('https://cwsqxbwez7.execute-api.us-east-1.amazonaws.com/Prod/counter/', {
            method: 'GET',
        }).then((response) => {
            console.log(response);
            response.json().then((data) => {
                console.log(data);
                document.getElementById("Visitors").innerHTML = "Views:    " + data["Visitors"];
            });
        });
    } catch (err) {
        console.error(err);
    }
}

getNumVisitors();