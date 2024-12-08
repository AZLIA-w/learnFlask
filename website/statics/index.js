function deleteNote(noteId) {
    fetch("/delete-note", {
      method: "POST",
      body: JSON.stringify({ noteId: noteId }),
    }).then((_res) => {
        // 通过再次访问homepage都达成刷新页面
      window.location.href = "/";
    });
  }