function getAll(){
    var request = new XMLHttpRequest;
    request.open('get','http://localhost:8000/contactos');
    request.send();

    request.onload = (e) => {
        const response = request.responseText;
        const json = JSON.parse(response);
        console.log("response" + json.response)
    };
}