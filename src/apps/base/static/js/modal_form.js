; (function () {

  const baseModal = document.querySelector('#baseModal');
  const modal = new bootstrap.Modal(baseModal);
  const baseModalContent = document.querySelector('#baseModalContent');

  // const offcanvasForm = document.querySelector('#offcanvasForm');
  // const offcanvas = new bootstrap.Offcanvas(offcanvasForm);

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
  htmx.on("closeModal", () => { modal.hide() })

  // Permission to OffcanvasForm
  // htmx.on('htmx:beforeSwap', function (evt) {
  //   if (evt.detail.xhr.status === 403) {
  //     alert(JSON.parse(evt.detail.xhr.response)['message']);
  //   } else {
  //     offcanvas.show()
  //   }
  // });

  // Remove #baseModalContent content after hiding
  baseModal.addEventListener('hidden.bs.modal', () => {
    baseModalContent.innerHTML = '';
  });

})()