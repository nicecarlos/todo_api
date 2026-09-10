document.addEventListener("DOMContentLoaded", () => {

// ==========================
// ELEMENTOS DA PÁGINA
// ==========================

const loginSection = document.getElementById("login-section");
const registerSection = document.getElementById("register-section");

const showRegister = document.getElementById("show-register");
const showLogin = document.getElementById("show-login");

const loginForm = document.getElementById("login-form");
const registerForm = document.getElementById("register-form");

// Elementos do modal
const authModal = document.getElementById("auth-modal");
const authModalTitle = document.getElementById("auth-modal-title");
const authModalMessage = document.getElementById("auth-modal-message");
const authModalOk = document.getElementById("auth-modal-ok");


// ==========================
// MOSTRAR MENSAGEM
// ==========================

function showMessage(title, message) {

    authModalTitle.textContent = title;
    authModalMessage.textContent = message;

    authModal.style.display = "flex";
}


// ==========================
// FECHAR MENSAGEM
// ==========================

authModalOk.addEventListener("click", () => {

    authModal.style.display = "none";

});


// ==========================
// MOSTRAR CADASTRO
// ==========================

showRegister.addEventListener("click", (event) => {

    event.preventDefault();

    loginSection.style.display = "none";
    registerSection.style.display = "block";

});


// ==========================
// MOSTRAR LOGIN
// ==========================

showLogin.addEventListener("click", (event) => {

    event.preventDefault();

    registerSection.style.display = "none";
    loginSection.style.display = "block";

});


// ==========================
// LOGIN
// ==========================

loginForm.addEventListener("submit", async (event) => {

    event.preventDefault();

    const email = document
        .getElementById("login-email")
        .value
        .trim();

    const password = document
        .getElementById("login-password")
        .value;

    try {

        const response = await fetch("/api/users/login", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                email: email,
                password: password
            })

        });

        const data = await response.json();

        if (response.ok) {

            // Login realizado com sucesso
            window.location.href = "/tasks";

        } else {

            showMessage(
                "Erro no login",
                data.error || "E-mail ou senha incorretos."
            );

        }

    } catch (error) {

        console.error("Erro ao realizar login:", error);

        showMessage(
            "Erro",
            "Não foi possível conectar ao servidor."
        );

    }

});


// ==========================
// CADASTRO
// ==========================

registerForm.addEventListener("submit", async (event) => {

    event.preventDefault();

    const name = document
        .getElementById("register-name")
        .value
        .trim();

    const email = document
        .getElementById("register-email")
        .value
        .trim();

    const password = document
        .getElementById("register-password")
        .value;

    try {

        const response = await fetch("/api/users", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                name: name,
                email: email,
                password: password
            })

        });

        const data = await response.json();

        if (response.ok) {

            // Limpa o formulário
            registerForm.reset();

            // Volta para a tela de login
            registerSection.style.display = "none";
            loginSection.style.display = "block";

            // Mostra mensagem de sucesso
            showMessage(
                "Conta criada",
                "Sua conta foi criada com sucesso! Agora você pode fazer login."
            );

        } else {

            showMessage(
                "Erro ao criar conta",
                data.error || "Não foi possível criar sua conta."
            );

        }

    } catch (error) {

        console.error("Erro ao criar conta:", error);

        showMessage(
            "Erro",
            "Não foi possível conectar ao servidor."
        );

    }

});
});