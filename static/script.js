// dominant
// auxiliary
// tertiary
// inferior

function submitCurrentState() {
    var dominant = document.getElementById("dominant").value;
    var auxiliary = document.getElementById("auxiliary").value;
    var tertiary = document.getElementById("tertiary").value;
    var inferior = document.getElementById("inferior").value;

    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/api/submitCurrentstate", true);
    xhr.setRequestHeader('Content-Type', 'application/json');

    return new Promise((resolve, reject) => {
        xhr.onload = function() {
            if (xhr.status >= 200 && xhr.status < 300) {
                resolve(xhr.response);
            } else {
                reject(xhr.statusText);
            }
        };

        xhr.onerror = function() {
            reject(xhr.statusText);
        };

        xhr.send(JSON.stringify({
            dominant: dominant,
            auxiliary: auxiliary,
            tertiary: tertiary,
            inferior: inferior
        }));
    }).then(res => {
        console.log("Request complete! response:", res);
    }).catch(error => {
        console.error("Request failed:", error);
    });
}