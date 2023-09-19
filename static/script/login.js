document.addEventListener("DOMContentLoaded", function () {
  const senhaInput = document.querySelector("input[name='senha']");
  const senhaLabel = document.getElementById("senhaLabel");
  const eyeIcon = document.getElementById("verSenha");
  const gerarSenhaBtn = document.getElementById("gerarSenhaBtn");

  eyeIcon.addEventListener("click", function () {
      if (senhaInput.type === "password") {
          senhaInput.type = "text";
          senhaLabel.textContent = "Senha Visível"; // Ou qualquer outro texto que você desejar
          eyeIcon.classList.remove("fa-eye");
          eyeIcon.classList.add("fa-eye-slash");
      } else {
          senhaInput.type = "password";
          senhaLabel.textContent = "Senha"; // Volte ao rótulo original
          eyeIcon.classList.remove("fa-eye-slash");
          eyeIcon.classList.add("fa-eye");
      }
  });

  gerarSenhaBtn.addEventListener("click", function () {
      senhaInput.value = gerarSenhaAleatoria(); // Chame sua função de geração de senha aqui
  });
});
