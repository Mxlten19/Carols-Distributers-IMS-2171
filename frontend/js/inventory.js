//---------------------------------------------
// CONSTANTS
//---------------------------------------------
const DEFAULT_CATEGORIES = [
    'FOOD',
    'BEVERAGES',
    'HOUSEHOLD ITEMS',
    'CLEANING SUPPLIES',
    'TOILETRIES',
    'MISCELLANEOUS'
];

//---------------------------------------------
// LOAD ALL PRODUCTS INTO TABLE
//---------------------------------------------
async function loadProducts() {

    let data = await apiGet("/inventory/");
    let table = document.getElementById("product-table");

    table.innerHTML = "";

    data.forEach(p => {

        table.innerHTML += `
            <tr>
                <td>${p.id}</td>
                <td>${p.name}</td>
                <td>$${p.price}</td>
                <td>${p.qty}</td>
                <td>${p.category}</td>
                <td>
                    <button class="btn-secondary" onclick="viewProductDetails('${p.product_id}')">
                        View
                    </button>
                </td>
            </tr>
        `;

    });
}

//---------------------------------------------
// FETCH CATEGORIES
//---------------------------------------------
async function fetchCategories(){
    return DEFAULT_CATEGORIES;
}

//---------------------------------------------
// OPEN ADD PRODUCT MODAL
//---------------------------------------------
async function openAddProductModal(){

    document.getElementById("modal-title").innerText = "Add Product";

    let categories = await fetchCategories();

    let opts = categories
        .map(c => `<option value="${c}">${c}</option>`)
        .join("");

    document.getElementById("modal-body").innerHTML = `
        <input id="p-name" placeholder="Product Name" class="input" />
        <input id="p-price" placeholder="Price" type="number" class="input" />
        <input id="p-qty" placeholder="Quantity" type="number" class="input" />
        <input id="p-threshold" placeholder="Reorder Threshold" type="number" class="input" />

        <select id="p-category" class="input">
            <option disabled selected>Select Category</option>
            ${opts}
        </select>
    `;

    document.getElementById("modal-save-btn").onclick = addProduct;

    openModal();
}

//---------------------------------------------
// ADD PRODUCT 
//---------------------------------------------
async function addProduct(){

    clearError();

    let name = document.getElementById("p-name");
    let price = document.getElementById("p-price");
    let qty = document.getElementById("p-qty");
    let threshold = document.getElementById("p-threshold");
    let category = document.getElementById("p-category");

    let data = {
        name: name.value.trim(),
        price: parseFloat(price.value),
        quantity: parseInt(qty.value),
        reorder_threshold: parseInt(threshold.value),
        category: category.value
    };

    let res = await apiPost("/inventory/product", data);

    if(res?.error){

        showFormError(res.error);

        // highlights problem fields
        if (!data.name) markError("p-name");
        if (isNaN(data.price)) markError("p-price");
        if (isNaN(data.quantity)) markError("p-qty");
        if (isNaN(data.reorder_threshold)) markError("p-threshold");
        if (!data.category) markError("p-category");

        return;
    }

    alert(res.message);

    closeModal();
    loadProducts();
}


//---------------------------------------------
// SELECT PRODUCT TO EDIT
//---------------------------------------------
async function openSelectProductForEdit(){

    let products = await apiGet("/inventory/");

    let dropdown = `
        <select id="product-select" class="input">
            ${products.map(p => 
                `<option value="${p.product_id}">${p.name}</option>`
            ).join("")}
        </select>
    `;

    document.getElementById("modal-title").innerText = "Select Product to Edit";
    document.getElementById("modal-body").innerHTML = dropdown;

    document.getElementById("modal-save-btn").onclick = () => {

        let id = document.getElementById("product-select").value;

        let selected = products.find(p => 
            String(p.product_id) === String(id)
        );

        openEditProductModal(selected);
    };

    openModal();
}

//---------------------------------------------
// OPEN EDIT PRODUCT MODAL
//---------------------------------------------
async function openEditProductModal(product){

    document.getElementById("modal-title").innerText = "Edit Product";

    let categories = await fetchCategories();

    let opts = categories.map(c =>
        `<option value="${c}" ${c === product.category ? "selected" : ""}>${c}</option>`
    ).join("");

    document.getElementById("modal-body").innerHTML = `
        <input id="p-name" value="${product.name}" class="input" />
        <input id="p-price" value="${product.price}" type="number" class="input" />
        <input id="p-qty" value="${product.qty}" type="number" class="input" />
        <input id="p-threshold" value="${product.reorder_threshold ?? ""}" type="number" class="input" />

        <select id="p-category" class="input">
            ${opts}
        </select>
    `;

    document.getElementById("modal-save-btn").onclick = () =>
        updateProduct(product.product_id);

    openModal();
}

//---------------------------------------------
// UPDATE PRODUCT
//---------------------------------------------
async function updateProduct(id){

    let data = {
        name: document.getElementById("p-name").value,
        price: parseFloat(document.getElementById("p-price").value),
        current_quantity: parseInt(document.getElementById("p-qty").value),
        reorder_threshold: parseInt(document.getElementById("p-threshold").value),
        category: document.getElementById("p-category").value
    };

    let res = await apiPut(`/inventory/product/${id}`, data);

    if(res.error){
        alert(res.error);
        return;
    }

    alert(res.message);

    closeModal();
    loadProducts();
}

// ---------------------------------------------
// SELECT PRODUCT TO DELETE
// ---------------------------------------------
async function openSelectProductForDelete() {
    let products = await apiGet("/inventory/");

    document.getElementById("modal-title").innerText = "Remove Product";

    document.getElementById("modal-body").innerHTML = `
        <select id="product-select" class="input">
            ${products.map(p =>
                `<option value="${p.product_id}">${p.name}</option>`
            ).join("")}
        </select>
        <p style="margin-top:12px; color:#c0392b; font-weight:bold;">
            Are you sure you want to delete this product? This cannot be undone.
        </p>
    `;

    document.getElementById("modal-save-btn").style.display = "inline-block";
    document.getElementById("modal-save-btn").innerText = "Delete";
    document.getElementById("modal-save-btn").onclick = async () => {
        let id = document.getElementById("product-select").value;
        await deleteProduct(id);
    };

    openModal();
}


// ---------------------------------------------
// DELETE PRODUCT
// ---------------------------------------------
async function deleteProduct(id) {
    let res = await apiDelete(`/inventory/product/${id}`);

    if (!res || res.error) {
        alert(res ? res.error : "Delete failed. Please try again.");
        return;
    }

    alert(res.message);

    document.getElementById("modal-save-btn").innerText = "Save";
    closeModal();
    loadProducts();
}


//---------------------------------------------
// PRODUCT VIEW
//---------------------------------------------
async function viewProductDetails(productId){

    let products = await apiGet("/inventory/");

    let product = products.find(p =>
        p.product_id == productId
    );

    if(!product) return;

    document.getElementById("modal-title").innerText = "Product Details";

    document.getElementById("modal-body").innerHTML = `
        <p><strong>Product ID:</strong> ${product.id}</p>
        <p><strong>Name:</strong> ${product.name}</p>
        <p><strong>Price:</strong> $${product.price}</p>
        <p><strong>Quantity:</strong> ${product.qty}</p>
        <p><strong>Threshold:</strong> ${product.reorder_threshold || "N/A"}</p>
        <p><strong>Category:</strong> ${product.category}</p>
    `;

    document.getElementById("modal-save-btn").style.display = "none";

    openModal();
}

//---------------------------------------------
// MODAL HELPERS
//---------------------------------------------
function openModal(){
    document.getElementById("modal").classList.remove("hidden");
}

function closeModal(){
    document.getElementById("modal").classList.add("hidden");
    document.getElementById("modal-save-btn").style.display = "inline-block";
}

//---------------------------------------------
// EVENT LISTENERS
//---------------------------------------------
document.addEventListener("DOMContentLoaded", () => {

    loadProducts();

    document.getElementById("add-product-btn")
        .addEventListener("click", openAddProductModal);

    document.getElementById("edit-product-btn")
        .addEventListener("click", openSelectProductForEdit);

    document.getElementById("remove-product-btn")
        .addEventListener("click", openSelectProductForDelete);

});

function markError(fieldId) {
    const el = document.getElementById(fieldId);
    if (!el) return;

    el.classList.add("input-error");

    el.addEventListener("input", () => {
        el.classList.remove("input-error");
        clearError();
    });
}

function showFormError(message) {
    let banner = document.getElementById("form-error");

    if (!banner) {
        banner = document.createElement("div");
        banner.id = "form-error";
        banner.className = "error-banner";

        document.getElementById("modal-body")
            .prepend(banner);
    }

    banner.innerText = message;
}

function clearError() {
    const b = document.getElementById("form-error");
    if (b) b.remove();
}