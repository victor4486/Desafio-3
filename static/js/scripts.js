function abrirModal(titulo, texto) {
    // Atualiza o título e o texto do modal
    document.getElementById("modal-title").innerText = titulo;
    document.getElementById("modal-text").innerText = texto;

    // Mostra o modal e o overlay
    document.getElementById("overlay").style.display = "block"; 
    document.getElementById("modal").style.display = "block"; 
}

function fecharModal() {
    // Oculta o modal e o overlay
    document.getElementById("overlay").style.display = "none";
    document.getElementById("modal").style.display = "none";
}
