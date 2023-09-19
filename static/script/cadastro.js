"use stict"

// cadastro.js

document.addEventListener("DOMContentLoaded", function () {
    const gerarSenhaBtn = document.getElementById("gerarSenhaBtn");
    const senhaInput = document.getElementById("senha1");
  
    gerarSenhaBtn.addEventListener("click", function () {
      const senhaAleatoria = gerarSenha();
      senhaInput.value = senhaAleatoria;
    });
  
    function gerarSenha() {
      const caracteres = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()";
      const tamanhoSenha = 12; // Defina o tamanho da senha desejado
      let senha = "";
  
      for (let i = 0; i < tamanhoSenha; i++) {
        const randomIndex = Math.floor(Math.random() * caracteres.length);
        senha += caracteres.charAt(randomIndex);
      }
  
      return senha;
    }
  });

// login.js
document.addEventListener("DOMContentLoaded", function () {
  const senhaInput = document.getElementById("senha");
  const eyeIcon = document.getElementById("verSenha");

  eyeIcon.addEventListener("click", function () {
      if (senhaInput.type === "password") {
          senhaInput.type = "text";
          eyeIcon.classList.remove("fa-eye");
          eyeIcon.classList.add("fa-eye-slash");
      } else {
          senhaInput.type = "password";
          eyeIcon.classList.remove("fa-eye-slash");
          eyeIcon.classList.add("fa-eye");
      }
  });
});

function togglePasswordVisibility(id) {
  var senhaInput = document.getElementById(id);
  var passwordToggle = document.querySelector(".password-toggle");

  if (senhaInput.type === "password") {
    senhaInput.type = "text";
    passwordToggle.textContent = "Ocultar";
  } else {
    senhaInput.type = "password";
    passwordToggle.textContent = "Mostrar";
  }
}

document.getElementById("senha2").addEventListener("input", function () {
  var senha1 = document.getElementById("senha1").value;
  var senha2 = document.getElementById("senha2").value;
  var errorMessage = document.getElementById("error-message");

  if (senha1 !== senha2) {
    errorMessage.textContent = "As senhas não coincidem.";
  } else {
    errorMessage.textContent = "";
  }
});

