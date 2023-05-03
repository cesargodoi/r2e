;(function () {

  var myModal = new bootstrap.Modal(document.getElementById('baseModal'))

  // Response targeting #baseModalContent => show the modal
  htmx.on("#baseModal", "htmx:afterSwap", (event) => {
    if (event.detail.target.id == "baseModalContent") {
      $('#baseModal').modal('show');
    }
  })
  
  // Empty response targeting #baseModalContent => hide the modal
  htmx.on("#baseModal", "htmx:beforeSwap", (event) => {
    if (event.detail.target.id == "baseModalContent" && !event.detail.xhr.response) {
      $('#baseModal').modal('hide');
    }
  })

  // Close modal by event
  htmx.on("closeModal", () => {modalForm.hide()})
  
  // Close modal (old style)
  htmx.on("#baseModal", "htmx:beforeSend", (e) => {
    $('#baseModal').modal('hide');
  });

  // Remove #baseModalContent content after hiding
  htmx.on("#baseModal", "hidden.bs.modal", () => {
    $("#baseModalContent").empty();
  })
})()