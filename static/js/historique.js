// static/js/historique.js
document.addEventListener('DOMContentLoaded', function() {
    var historiqueContainer = document.getElementById('historique-container');

    if (historiqueContainer) {
        historiqueContainer.addEventListener('click', function(event) {
            if (event.target.classList.contains('supprimer-document')) {
                var docId = event.target.getAttribute('data-doc-id');
                
                if (confirm('Êtes-vous sûr de vouloir supprimer ce document?')) {
                    fetch('/supprimer_document', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({ id: docId })
                    })
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            var docItem = document.querySelector(`[data-doc-id="${docId}"]`);
                            if (docItem) {
                                docItem.remove();
                            }
                        } else {
                            alert('Erreur lors de la suppression du document.');
                        }
                    })
                    .catch(error => {
                        console.error('Erreur:', error);
                        alert('Erreur: ' + error.message);
                    });
                }
            }
        });
    } else {
        console.error('Element historique-container non trouvé dans le DOM');
    }
});
