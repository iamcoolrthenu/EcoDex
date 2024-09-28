class MyHeader extends HTMLElement {
    connectedCallback() {
        fetch("Template/Header.html")
            .then(response => response.text())
            .then(html => {
                this.innerHTML = html;
            });
    }
}

customElements.define('my-header', MyHeader)

class MyFooter extends HTMLElement {
    connectedCallback() {
        fetch('Template/Footer.html')
        .then(response => response.text())
        .then(html =>{
            this.innerHTML = html;
        })
    }   
}
window.addEventListener('load', () => {
    document.body.classList.add('loaded');
});

customElements.define('my-footer', MyFooter)
