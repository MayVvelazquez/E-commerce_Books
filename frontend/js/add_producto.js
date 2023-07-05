const btnCart = document.querySelector('.container-icon');
const containerCartProducts = document.querySelector(
    '.container-cart-products'
);

btnCart.addEventListener('click', () => {
    containerCartProducts.classList.toggle('hidden-cart');
});

const cartInfo = document.querySelector('.cart-product');
const rowProduct = document.querySelector('.row-product');

// Lista de todos los contenedores de productos
const productsList = document.querySelector('#app');

// Variable de arreglos de Productos
let allProducts = [];

const valorTotal = document.querySelector('.total-pagar');

const countProducts = document.querySelector('#contador-productos');

const cartEmpty = document.querySelector('.cart-empty');
const cartTotal = document.querySelector('.cart-total');

productsList.addEventListener('click', e => {
    if (e.target.classList.contains('btn')) {
        const product = e.target.parentElement;

        const infoProduct = {
            quantity: 1,
            title: product.querySelector('.card-title').textContent,
            // des: product.querySelector('.card-title').textContent,
            price: product.querySelector('.price').textContent,
        };

        const exits = allProducts.some(
			product => product.title === infoProduct.title
		);

        if (exits) {
            const products = allProducts.map(product =>{
                if (product.title === infoProduct.title) {
                    product.quantity++;
                    return product
                }else{
                    return product
                }
            })

            allProducts = [...products];

        }else{

            allProducts = [...allProducts, infoProduct];

        }

        
        showHTML();
    }
});

rowProduct.addEventListener('click', e =>{
    if (e.target.classList.contains('icon-close')) {
		const product = e.target.parentElement;
        const title = product.querySelector('path').textContent;

        allProducts = allProducts.filter(
            product => product.title !== title
        );
        showHTML();

        console.log(allProducts);

    }

});

const showHTML = () => {

    if (!allProducts.length) {
		cartEmpty.classList.remove('hidden');
		rowProduct.classList.add('hidden');
		cartTotal.classList.add('hidden');
	} else {
		cartEmpty.classList.add('hidden');
		rowProduct.classList.remove('hidden');
		cartTotal.classList.remove('hidden');
	}

    rowProduct.innerHTML = '';

    let total = 0;
	let totalOfProducts = 0;

    allProducts.forEach(product => {
        const containerProduct = document.createElement('div');
        containerProduct.classList.add('cart-product');

        containerProduct.innerHTML = `
                                <span id="id">${product.quantity}</span>
                                <span id="nombre">${product.title}</span>
                                <span id="price">${product.price}</span>
                                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"
                                    stroke-width="1.5" stroke="currentColor" class="icon-close">
                                    <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
                                </svg>
       `;

        rowProduct.append(containerProduct);

        total =
			total + parseInt(product.quantity * product.price.slice(7));

	    totalOfProducts = totalOfProducts + product.quantity;

    });

    valorTotal.innerText = `$${total}`;
	// countProducts.innerText = totalOfProducts;

};