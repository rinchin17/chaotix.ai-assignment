const btn = document.getElementById('btn');
const form = document.getElementById('form');

form.addEventListener("submit", (event) => {
    // preventing the page to reload on submit
    event.preventDefault();

    //  fetching the values for the prompts
    let p1 = document.getElementById('prompt1').value;
    let p2 = document.getElementById('prompt2').value;
    let p3 = document.getElementById('prompt3').value;

    // disabling the generate button while the request is being completed
    btn.disabled = true;
    btn.style.cursor = "not-allowed";

    // adding loading animation to the images
    for (let i = 0; i < 3; i++) {
        let imgId = `img${i + 1}`;
        document.getElementById(`card${i + 1}`).classList.add("is-loading");
        document.getElementById(imgId).style.visibility = "hidden";
    }

    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    // calling an internal API which in turn calls the Stability API, sending the prompts in body
    fetch('/image/generate-image/', {
        method: "POST",

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
                //  setting the generated images
                let image = document.getElementById(`img${i + 1}`);
                let p = document.getElementById(`p${i + 1}`);
                document.getElementById(`card${i + 1}`).classList.remove("is-loading");
                image.src = url;
                image.style.visibility = "visible";
                p.innerHTML = document.getElementById(`prompt${i + 1}`).value;
            });
        })
        .catch(error => {
            alert("An error occured while generating the images");
            console.error('There was a problem with the fetch operation:', error);
        })
        .finally(() => {
            // fetch operation completed
            btn.disabled = false;
            btn.style.cursor = "pointer";
        });
});