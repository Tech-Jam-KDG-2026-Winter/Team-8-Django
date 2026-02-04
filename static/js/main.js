// プロフィール画像のプレビュー機能
document.addEventListener('DOMContentLoaded', function() {
  const profileInput = document.getElementById('profileImageInput');
  const profilePreview = document.getElementById('profilePreview');
  
  if (profileInput && profilePreview) {
    profileInput.addEventListener('change', function(e) {
      const file = e.target.files[0];
      
      if (file && file.type.startsWith('image/')) {
        const reader = new FileReader();
        
        reader.onload = function(e) {
          profilePreview.src = e.target.result;
        };
        
        reader.readAsDataURL(file);
      }
    });
  }

  // 投稿画像のプレビュー機能
  const imageInput = document.getElementById('imageInput');
  const imagePreview = document.getElementById('imagePreview');
  const imagePreviewContainer = document.getElementById('imagePreviewContainer');
  
  if (imageInput && imagePreview && imagePreviewContainer) {
    imageInput.addEventListener('change', function(e) {
      const file = e.target.files[0];
      
      if (file && file.type.startsWith('image/')) {
        const reader = new FileReader();
        
        reader.onload = function(e) {
          imagePreview.src = e.target.result;
          imagePreviewContainer.classList.add('has-image');
        };
        
        reader.readAsDataURL(file);
      }
    });
  }
});
