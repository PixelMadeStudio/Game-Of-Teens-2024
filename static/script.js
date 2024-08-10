console.log('Я працюю');
const routes = [
    { path: '/register', handler: signupHandler },
    { path: '/login', handler: loginHandler },
    { path: '/reg', handler: regHandler },
    { path: '/game', handler: gameHandler },
    { path: '/reset-password', handler: resetPasswordHandler }];

function RequestToServer(form, url) {
    const formData = new FormData(form);
    console.log('Sending request to server...');
    formData.append('key1', 'value1'); // Ensure this is required

    return new Promise((resolve, reject) => {
        fetch(url, {
            method: "POST",
            body: formData,
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => resolve(data))
        .catch(error => {
            console.error('Error:', error);
            reject(error);
        });
    });
}

function forgotPassword() {
    RequestToServer(document.getElementById('login-form'), '/forgot-password_')
    .then(response => {
        console.log(response);
        document.getElementById('lresult').innerHTML = `${response.message}`;
    });
}

function resetPasswordHandler() {
    const urlResetPassword = '/reset-password_';
    const res = document.getElementById('result');
    console.log('Я resetPasswordHandler');
    const resetForm = document.getElementById('reset-form');
    resetForm.addEventListener('submit', (event) => {
        event.preventDefault();
        RequestToServer(event.target, urlResetPassword)
        .then(response => {
            res.innerHTML = `${response.message}`;
        });
    });
}


function gameHandler() {
    const urlGame = '/game_';
    const form = document.getElementById('form');
    const res = document.getElementById('result');
    console.log('Я gameHandler1');
    form.addEventListener('submit', (event) => {
        event.preventDefault();
        RequestToServer(event.target, urlGame)
        .then(response => {
            res.innerHTML = `<p>${response.message}</p>`;
        });
    });
    console.log('Я gameHandler2');
    const commentsForm = document.querySelector('#comments-form');
    const urlComments = '/comments_';
    const resComments = document.getElementById('comments-result');
    commentsForm.addEventListener('submit', (event) => {
        event.preventDefault();
        RequestToServer(event.target, urlComments)
        .then(response => {
            resComments.innerHTML = `${response.message}`;
        });
    });
    console.log('Я commentsHandler');
}

function profileHandler() {
    const urlProfile = '/profile_';
    const res = document.getElementById('result1');
    const infoForm = document.querySelector('#update-info');
    console.log('Я profileHandler');
    infoForm.addEventListener('submit', (event) => {
        event.preventDefault();
        RequestToServer(event.target, urlProfile)
        .then(response => {
            res.innerHTML = `<p>${response.message}</p>`;
        });
    });
}

function regHandler() {
    const signupForm = document.querySelector('#signup-form');
    const loginForm = document.querySelector('#login-form');
    const sresult = document.getElementById('sresult');
    const lresult = document.getElementById('lresult');
    const urlSignLogin = '/reg_';
    console.log('Я regHandler');
    signupForm.addEventListener('submit', (event) => {
        event.preventDefault();
        RequestToServer(event.target, urlSignLogin)
        .then(response => {
            sresult.innerHTML = `<p>${response.message}</p>`;
        });
    });
    loginForm.addEventListener('submit', (event) => {
        event.preventDefault();
        RequestToServer(event.target, urlSignLogin)
        .then(response => {
            lresult.innerHTML = `<p>${response.message}</p>`;
        });
    });
}

function searchHandler() {
    const Form = document.querySelector('#FORM');
    const urlSearch = '/search';
    const res = document.getElementById('result');
    console.log('Я searchHandler');
    // Form.addEventListener('submit', (event) => {
    console.log('test')
    // event.preventDefault();
    RequestToServer(Form, urlSearch)
    
    .then(response => {
        res.innerHTML = `<p>${response.message}</p>`;
        // });
    });
    
}



function signupHandler() {
    const Form = document.querySelector('#signup-form');
    const urlSignup = '/signup_';
    const res = document.getElementById('result');
    console.log('Я signupHandler');
    Form.addEventListener('submit', (event) => {
        event.preventDefault();
        RequestToServer(event.target, urlSignup)
        .then(response => {
            res.innerHTML = `<p>${response.message}</p>`;
        });
    });
}

function loginHandler() {
    const Form = document.querySelector('#login-form');
    const urlLogin = '/login_';
    const res = document.getElementById('result');
    console.log('Я loginHandler');
    Form.addEventListener('submit', (event) => {
        event.preventDefault();
        RequestToServer(event.target, urlLogin)
        .then(response => {
            res.innerHTML = `<p>${response.message}</p>`;
        });
    });
}



function addNote() {
    const urlAddNote = '/notes_';
    const res = document.getElementById('result');
    console.log('Я addNote');
    const addNoteForm = document.querySelector('#add-note');

    RequestToServer(addNoteForm, urlAddNote)
    .then(response => {
        res.innerHTML = `<p>${response.message}</p>`;
    });
    }
    // location.reload()

function notesHandler() {
    const urlNotes = '/notes__';
    const res = document.getElementById('result');
    console.log('Я notesHandler');
    const count = document.getElementById('count');
    
    for (let i = 1; i < count.value+1; i++) {
        try {
        console.log(i)
        const notesForm = document.querySelector('#notes-form'+i);
        RequestToServer(notesForm, urlNotes)
        .then(response => {
            res.innerHTML = `<p></p>`;
        });
        }catch(error){
            console.log(error)
        }
    }
}

function Request2Server(form, url) {
    const formData = new FormData();
    console.log('Sending request 2 server...');
    formData.append('id', form); // Ensure this is required

    return new Promise((resolve, reject) => {
        fetch(url, {
            method: "POST",
            body: formData,
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => resolve(data))
        .catch(error => {
            console.error('Error:', error);
            reject(error);
        });
    });
}


function DelNotesHandler(id) {
    const urlNotes = '/notes_del_';
    const res = document.getElementById('result');
    console.log('Я notesHandler');
    const count = document.getElementById('count');
    
    
    const notesForm = document.querySelector('#notes-form');
    Request2Server(notesForm, urlNotes)
    .then(response => {
        res.innerHTML = `<p></p>`;
    });
    
}


function handleRoutes() {
    const currentPath = window.location.pathname;
    console.log('Я  handleRoutes');
    const routeData = routes.find(route => route.path === currentPath);
    routeData.handler();
};


function mystHandler() {
    const result = document.getElementById('result');
    console.log('Я mystHandler');

    result.innerHTML = `<div class="game-card">
            <a href="/happybara_mystery"><img src="/capybara/gameover.jpg" alt="Img Not Found" /></a>
            <div class="">

            <h3><a href="/happybara_mystery" class="game-title happybara-card">H<p class="notread">A</p>PPYBARA</a></h3>
            </div>
            <p class="notread">asdafdfsdfsdfdsggsdgfdgdfgdfggasfdgfdfvabgdbgdfb</p>

        </div>`;

}



document.addEventListener("DOMContentLoaded", function() {
    handleRoutes();
});

