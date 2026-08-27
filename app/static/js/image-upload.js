document.querySelectorAll('.image-upload').forEach((upload) => {
    const input = upload.querySelector('.image-input');
    const preview = upload.querySelector('.image-preview');
    const fileName = upload.querySelector('.file-name');

    input.addEventListener('change', () => {
        const file = input.files[0];

        if (!file) {
            return;
        }

        fileName.textContent = file.name;
        preview.src = URL.createObjectURL(file);
    });
});