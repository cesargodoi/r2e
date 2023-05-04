; (function () {

  const baseModal = document.querySelector('#baseModal');
  const modal = new bootstrap.Modal(baseModal);
  const baseModalContent = document.querySelector('#baseModalContent');

  // Response targeting #baseModalContent => show the modal
  baseModal.addEventListener('htmx:afterSwap', (event) => {
    if (event.detail.target.id === 'baseModalContent') {
      modal.show();
    }
  });

  // Empty response targeting #baseModalContent => hide the modal
  baseModal.addEventListener('htmx:beforeSwap', (event) => {
    if (event.detail.target.id === 'baseModalContent' && !event.detail.xhr.response) {
      modal.hide();
    }
  });

  // Close modal by event
  htmx.on("closeModal", () => { modalForm.hide() })

  // Close modal (old style)
  htmx.on("#baseModal", "htmx:beforeSend", (e) => {
    modal.hide();
  });

  // Remove #baseModalContent content after hiding
  baseModal.addEventListener('hidden.bs.modal', () => {
    baseModalContent.innerHTML = '';
  });

})()