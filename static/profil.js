console.log('Зайшло');
const routes = [

    { path: '/profile', handler: Prof_h },
];

function RequestToServer(form, url) {
    const formData = new FormData(form);
    console.log('Запит для серверу');
    formData.append('key1', 'value1');

    return new Promise((resolve, reject) => {
        fetch(url, {
            method: "POST",
            body: formData,
        })
        .then(response => response.json())
        .then(data => {
            resolve(data);
        });
    });
}




function Prof_h() {
    console.log("popup");
    // const formmm = document.querySelector('#form3');
    // const urlLogin = '/prot3';
    // console.log('Я buy_reg');

    // RequestToServer(formmm, urlLogin)
    //     .then(response => {
    //         res.innerHTML = '';
    //         response.message.forEach(info => {
    //         res.innerHTML = `
    //             <h1>${info.u_nme}</h1>
    //             <h3>${info.psevdo}</h3>
    //             <p>${info.u_info}</p>`;
    //     });
    //   });

    const popup = document.getElementById("popup");
    const openBtn = document.getElementById("open_pop");
    openBtn.addEventListener('click', function(){
        popup.classList.add("active");
        console.log("popup");
    });

    const closeBtn = document.getElementById("close-btn");

    closeBtn.addEventListener('click', function(){
        popup.classList.remove("active");

    });

    const res = document.getElementById('res');
    const form = document.querySelector('#form3');

    form.addEventListener('submit', (event) => {
        event.preventDefault();
        popup.classList.remove("active");
        RequestToServer(event.target, urlLogin)
            .then(response => {
            res.innerHTML = '';
            response.message.forEach(info => {
            res.innerHTML = `
                <h1>${info.u_nme}</h1>
                <h3>${info.psevdo}</h3>
                <p>${info.u_info}</p>`;

        });
    });
    });

    // Ця частина відповідає за бібліотеку

    const lib_all = document.getElementById("lib_all");

    close_lib.addEventListener('click', function(){
        lib_all.style.display = "none";

    });

}

function profileHandler() {
    const popup = document.getElementById("popup");
    const urlProfile = '/profile_';
    const res = document.getElementById('result_');
    const infoForm = document.querySelector('#update-info');
    console.log('Я profileHandler');
    // popup.classList.remove("active");
    RequestToServer(infoForm, urlProfile)
    .then(response => {
        
        res.innerHTML = `<p class="italic success">saved</p>`;
    });
}

function openLib() {
    const lib_all = document.getElementById("lib_all");
    lib_all.style.display = "block";
}



function closeLib() {
    const lib_all = document.getElementById("lib_all");
    lib_all.style.display = "none";
}


function handleRoutes() {
    const currentPath = window.location.pathname;
    console.log('Я  handleRoutes');
    const routeData = routes.find(route => route.path === currentPath);
    routeData.handler();
};


function removeFromLib() {
    const urlRemoveFromLib = '/remove-from-lib_';
    const res = document.getElementById('res');
    console.log('Я removeFromLib');
    const remForm = document.querySelector('#rem-from-lib');
    RequestToServer(remForm, urlRemoveFromLib)
    .then(response => {
        res.innerHTML = `<p class="italic success">removed from library</p>`;
    });
}


document.addEventListener("DOMContentLoaded", function() {
    handleRoutes();
});