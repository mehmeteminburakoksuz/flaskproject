function deleteNote(noteId) {
  fetch("/delete-note", {
    method: "POST",
    body: JSON.stringify({ noteId: noteId }),
  }).then((_res) => {
    window.location.href = "/";
  });
}
document.addEventListener('DOMContentLoaded', () => {
  document.getElementById('addSquareButton').addEventListener('click', () => {
      document.getElementById('addSquareForm').submit();
  });
});

function showContent(squareId) {
  window.location.href = `/square/${squareId}`;
}
