async function inscribir(id){
    var checkedBoxes = document.querySelectorAll('input[type=checkbox]:checked');
    var ids=[];
    checkedBoxes.forEach(
        function(node) {
            ids.push(node.id);
        }
    ) 

    const csrftoken = getCookie('csrftoken');
    var url = "/tutores/inscribir_alumno/"+id+"/";

    await fetch(url, {
        method: 'POST',
        credentials: 'same-origin',
        headers:{
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
    },
        body: JSON.stringify(Object.assign({}, ids)),
        
        }
    ).then(response => {
        return response.json();
}).then(data=> console.log(data),
window.location.reload(true));
}

async function desuscribir(id){
    var checkedBoxes = document.querySelectorAll('input[type=checkbox]:not(:checked)');
    var ids=[];
    checkedBoxes.forEach(
        function(node) {
            ids.push(node.id);
        }
    ) 

    const csrftoken = getCookie('csrftoken');
    var url = "/tutores/grupos_alumno/"+id+"/";

    await fetch(url, {
        method: 'POST',
        credentials: 'same-origin',
        headers:{
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
    },
        body: JSON.stringify(Object.assign({}, ids)),
        
        }
    ).then(response => {
        return response.json();
    }).then(data=> console.log(data),
    window.location.reload(true));
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}