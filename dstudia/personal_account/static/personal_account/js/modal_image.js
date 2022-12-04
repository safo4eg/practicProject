let applications = document.querySelectorAll('.recent-application');
let modalImage = document.getElementById('modal-image');
let modalImageContent = document.querySelector('.modal-image-content img');
let modalImageCaption = document.querySelector('.modal-image-caption');
let modalImageCloser = document.querySelector('.modal-image-close');

function showModalImageApplication(event) {
    let applicationName = this.querySelector('.recent-application-info li:first-child');
    let applicationImg = this.querySelector('.recent-application-img');

    modalImageCaption.textContent = applicationName.textContent;
    modalImageContent.src = applicationImg.src;
    modalImage.classList.add('show');
}

function closeModalImageApplication(event) {
    modalImage.classList.remove('show');
}

for(let application of applications) {
    application.addEventListener('click', showModalImageApplication);
}

modalImageCloser.addEventListener('click', closeModalImageApplication);