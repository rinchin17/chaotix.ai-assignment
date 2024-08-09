const btn = document.getElementById('btn');
btn.addEventListener("click", () => {
    console.log('btn');
    let p1 = document.getElementById('p1').value;
    let p2 = document.getElementById('p2').value;
    let p3 = document.getElementById('p3').value;
    if (!p1 || !p2 || !p3) {
        alert("Please fill in all the prompts.");
        return;
    }
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    fetch('/image/generate-image/', {
        method: "POST",

        // Adding body or contents to send 
        body: JSON.stringify({
            prompts: [p1, p2, p3]
        }),
        headers: {
            'Content-Type': 'application/json',
            accept: 'application/json',
            'X-CSRFToken': csrftoken
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        urls = data['image_urls'];
        urls.forEach((url, i) => {
            console.log(i)
            let imgId = `img${i + 1}`;
            document.getElementById(imgId).src = url;
        });
    })
    .catch(error => {
        alert("An error occured while generating the images");
        console.error('There was a problem with the fetch operation:', error);
    });
});