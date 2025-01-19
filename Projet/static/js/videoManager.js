function playVideo(video) {
    video.play();
}

function openVideo(video) {
  fetch("/video/", { //url de la requête
    method: "POST",
    body: JSON.stringify({ //DATA
      id: video.id
    }),
    headers: {
      "Content-type": "application/json; charset=UTF-8"
    }
  })
    .then((response) => response.json())
    .then((json) => console.log(json));
}