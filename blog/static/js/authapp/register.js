
  const avatarCircle = document.getElementById('avatarCircle');
  const avatarInput = document.getElementById('avatarInput');
  const avatarPreview = document.getElementById('avatarPreview');

  avatarCircle.addEventListener('click', function () {
    avatarInput.click(); // ouvre le stockage
  });

  avatarInput.addEventListener('change', function () {
    const file = this.files[0];
    if (file) {
      avatarPreview.src = URL.createObjectURL(file);
      avatarPreview.style.display = 'block';
      document.querySelector('.camera-icon').style.display = 'none';
    }
  });
