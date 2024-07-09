document.addEventListener('DOMContentLoaded', function() {
    var genererdocumentButton = document.getElementById('genererdocument');
    var form = document.getElementById('project-form');

    if (genererdocumentButton) {
        genererdocumentButton.addEventListener('click', function(event) {
            event.preventDefault();

            var spinnerModal = new bootstrap.Modal(document.getElementById('spinnerModal'), {
                backdrop: 'static',  // Empêche la fermeture du modal en cliquant à l'extérieur
                keyboard: false      // Empêche la fermeture du modal avec la touche Échap
            });
            spinnerModal.show();

            var nomProjet = document.getElementById('nom_projet').value;
            var descriptionProjet = document.getElementById('description_projet').value;
            var modelSelection = document.getElementById('modelSelection').value;

            console.log(nomProjet, descriptionProjet, modelSelection);

            // Déterminer l'endpoint en fonction du modèle sélectionné
            var endpoint = '';
            if (modelSelection === 'chatgpt') {
                endpoint = '/generer_documentation_chatgpt';
            } else if (modelSelection === 'ollama') {
                endpoint = '/generer_documentation_ollama';
            } else {
                endpoint = '/generer_documentation_other';
            }

            // Envoyer les données au serveur
            fetch(endpoint, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    nom_projet: nomProjet,
                    description_projet: descriptionProjet
                })
            })
            .then(response => {
                console.log(`HTTP status: ${response.status}`);
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                spinnerModal.hide();

                if (data.documentation) {
                    // Rediriger vers la page de résultat avec les données
                    window.location.href = `/result?documentation=${encodeURIComponent(data.documentation)}`;
                } else if (data.error) {
                    console.error('Erreur:', data.error);
                    alert('Erreur: ' + data.error);
                } else {
                    console.error('Erreur: Documentation non trouvée');
                    alert('Erreur: Documentation non trouvée');
                }
            })
            .catch(error => {
                spinnerModal.hide();
                console.error('Erreur:', error);
                alert('Erreur: ' + error.message);
            });
        });
    } else {
        console.error('Element genererdocument non trouvé dans le DOM');
    }
});
