const englishImgPath = "{{ url_for('static', filename='img/uk.png') }}";
const germanImgPath = "{{ url_for('static', filename='img/germany.png') }}";

let languageButton = document.getElementById('home-language-button');

languageButton.addEventListener('click', () => {
    let languageIcon = document.getElementById('home-language-button-icon');
    console.log(languageIcon.src.includes('uk.png'));
    console.log(germanImgPath)
    languageIcon.src.includes('uk.png') ? languageIcon.src = germanImgPath : languageIcon.src = englishImgPath;
});
