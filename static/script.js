document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('file').addEventListener('change', displayFileNameAndImage);
    document.getElementById('upload-form').addEventListener('submit', handleFormSubmit);
});

function displayFileNameAndImage() {
    const fileInput = document.getElementById('file');
    const fileName = document.getElementById('file-name');
    const preview = document.getElementById('preview');
    const file = fileInput.files[0];
    
    if (file) {
        fileName.textContent = file.name;
        const reader = new FileReader();
        reader.onload = function (e) {
            preview.src = e.target.result;
        };
        reader.readAsDataURL(file);
        preview.style.display = 'block';
    } else {
        fileName.textContent = '';
        preview.src = '';
        preview.style.display = 'none';
    }
}

function handleFormSubmit(event) {
    event.preventDefault(); // Prevent the default form submission
    const formData = new FormData(document.getElementById('upload-form'));

    document.querySelector('.upload-form').style.display = 'none';
    document.getElementById('loading').style.display = 'flex';

    $.ajax({
        url: '/',
        type: 'POST',
        data: formData,
        processData: false,
        contentType: false,
        success: function(response) {
            // Handle the file download
            const link = document.createElement('a');
            link.href = response.file_url;
            link.download = response.filename;
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);

            resetFormState();
        },
        error: function(jqXHR, textStatus, errorThrown) {

            let errorMessage;
            try {
                let errorResponse = JSON.parse(jqXHR.responseText);
                errorMessage = errorResponse.error;
            } catch (e) {
                errorMessage = "An unknown error occured"
            }
            alert('Error: ' + errorMessage);
            resetFormState();
        }
    });
}

function resetFormState() {
    document.querySelector('.upload-form').reset();
    document.querySelector('.upload-form').style.display = 'flex';
    document.getElementById('loading').style.display = 'none';
    document.getElementById('file-name').textContent = '';
    document.getElementById('preview').src = '';
    document.getElementById('preview').style.display = 'none';
}
