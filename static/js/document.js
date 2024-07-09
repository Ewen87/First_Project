// static/js/result.js

document.addEventListener('DOMContentLoaded', function() {
    var telechargerButton = document.getElementById('telecharger_document');
    
    if (telechargerButton) {
        telechargerButton.addEventListener('click', function() {
            var fileName = document.getElementById('file_name').value || 'documentation';
            var fileFormat = document.getElementById('file_format').value || 'txt';
            var documentation = document.getElementById('documentation_output').textContent;

            fetch('/telecharger_documentation', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    documentation: documentation,
                    file_name: fileName,
                    file_format: fileFormat
                })
            })
            .then(response => response.blob())
            .then(blob => {
                var link = document.createElement('a');
                link.href = URL.createObjectURL(blob);
                link.download = `${fileName}.${fileFormat}`;
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
            })
            .catch(error => {
                console.error('Erreur:', error);
                alert('Erreur: ' + error.message);
            });
        });
    } else {
        console.error('Element telecharger_document non trouvé dans le DOM');
    }
});
