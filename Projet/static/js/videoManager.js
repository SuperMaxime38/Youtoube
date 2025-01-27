function playVideo(video) {
  console.log("play video");
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

function likeVideo() {
  console.log("like video" + document.getElementsByTagName("video")[0].id);
  fetch("/video/like", { //url de la requête
    method: "POST",
    body: JSON.stringify({ //DATA
      id: document.getElementsByTagName("video")[0].id
    }),
    headers: {
      "Content-type": "application/json; charset=UTF-8"
    }
  })
    .then((response) => response.json())
    .then((json) => console.log(json));
}