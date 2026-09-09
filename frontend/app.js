// ---- Configuração ----
// Endereço onde a API (uvicorn) está rodando.
const API_BASE = "http://127.0.0.1:8000";

// ---- Autenticação (token salvo no navegador) ----
function salvarToken(token) {
  localStorage.setItem("cine_henrique_token", token);
}

function obterToken() {
  return localStorage.getItem("cine_henrique_token");
}

function limparSessao() {
  localStorage.removeItem("cine_henrique_token");
  localStorage.removeItem("cine_henrique_usuario");
}

function estaLogado() {
  return !!obterToken();
}

// Garante que a página só é vista por quem está logado.
// Se não estiver logado, manda para a tela de login.
function exigirLogin() {
  if (!estaLogado()) {
    window.location.href = "login.html";
  }
}

// ---- Chamada genérica à API, já incluindo o token quando existir ----
async function apiFetch(caminho, opcoes = {}) {
  const token = obterToken();
  const headers = {
    "Content-Type": "application/json",
    ...(opcoes.headers || {}),
  };
  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  let resposta;
  try {
    resposta = await fetch(`${API_BASE}${caminho}`, { ...opcoes, headers });
  } catch (erro) {
    throw new Error(
      "Não foi possível conectar à API. Verifique se o servidor (uvicorn) está rodando em " +
        API_BASE
    );
  }

  // Token expirado ou inválido -> volta pro login
  if (resposta.status === 401 && !caminho.startsWith("/auth/login")) {
    limparSessao();
    window.location.href = "login.html";
    throw new Error("Sessão expirada. Faça login novamente.");
  }

  if (!resposta.ok) {
    let detalhe = "Erro na requisição";
    try {
      const corpo = await resposta.json();
      detalhe = corpo.detail || detalhe;
    } catch (e) {
      // resposta sem corpo JSON
    }
    throw new Error(detalhe);
  }

  if (resposta.status === 204) return null;
  return resposta.json();
}

// ---- Barra de navegação (usada em todas as páginas) ----
function montarNavbar(elementoId) {
  const el = document.getElementById(elementoId);
  if (!el) return;

  const usuarioNome = localStorage.getItem("cine_henrique_usuario");
  const logado = estaLogado();

  el.innerHTML = `
    <a href="index.html" class="logo">🎬 Cine Henrique</a>
    <nav>
      ${
        logado
          ? `
            <span class="usuario">Olá, ${usuarioNome || "usuário"}</span>
            <a href="novo-filme.html">+ Cadastrar filme</a>
            <button id="btn-sair">Sair</button>
          `
          : `
            <a href="login.html">Entrar</a>
            <a href="cadastro.html">Criar conta</a>
          `
      }
    </nav>
  `;

  const btnSair = document.getElementById("btn-sair");
  if (btnSair) {
    btnSair.addEventListener("click", () => {
      limparSessao();
      window.location.href = "login.html";
    });
  }
}

function mostrarMensagem(elementoId, texto, tipo = "erro") {
  const el = document.getElementById(elementoId);
  if (!el) return;
  el.textContent = texto;
  el.className = `mensagem ${tipo}`;
  el.style.display = texto ? "block" : "none";
}
