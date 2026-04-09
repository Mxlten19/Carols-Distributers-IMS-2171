//---------------------------------------------
// GLOBALS
//---------------------------------------------
let productsList = [];
let cart = [];


//---------------------------------------------
// LOAD ALL PRODUCTS AT START
//---------------------------------------------
document.addEventListener("DOMContentLoaded", async () => {
    productsList = await apiGet("/inventory/");
    renderProductList(productsList);
    renderCart();
});


//---------------------------------------------
// SEARCH PRODUCTS 
//---------------------------------------------
function searchProducts() {
    let q = document.getElementById("search-bar").value.toLowerCase();
    let filtered = productsList.filter(p =>
        p.name.toLowerCase().includes(q)
    );
    renderProductList(filtered);
}


//---------------------------------------------
// RENDER PRODUCT GRID BUTTONS
//---------------------------------------------
function renderProductList(list) {
    let container = document.getElementById("product-buttons");
    container.innerHTML = "";

    list.forEach(p => {
        container.innerHTML += `
            <div class="product-button" onclick="addToCart('${p.product_id}')">
                <b>${p.name}</b><br>
                $${p.price}
            </div>
        `;
    });
}


//---------------------------------------------
// ADD ITEM TO CART
//---------------------------------------------
function addToCart(id) {
    let product = productsList.find(p => p.product_id == id);
    if (!product) return;

    let existing = cart.find(i => i.product_id == id);

    if (existing) {
        existing.qty++;
    } else {
        cart.push({
            product_id: product.product_id, 
            name: product.name,
            price: product.price,
            qty: 1
        });


    }

    renderCart();
}


//---------------------------------------------
// UPDATE CART UI
//---------------------------------------------
function renderCart() {
    let table = document.getElementById("checkout-items");
    table.innerHTML = "";

    let subtotal = 0;

    cart.forEach((item, index) => {
        let total = item.qty * item.price;
        subtotal += total;

        table.innerHTML += `
            <tr>
                <td>${item.name}</td>
                <td>
                    <button class="qty-btn" onclick="changeQty(${index}, -1)">-</button>
                    ${item.qty}
                    <button class="qty-btn" onclick="changeQty(${index}, 1)">+</button>
                </td>
                <td>$${total.toFixed(2)}</td>
            </tr>
        `;
    });

    let tax = subtotal * 0.15;
    let grand = subtotal + tax;

    document.getElementById("subtotal").innerText = `$${subtotal.toFixed(2)}`;
    document.getElementById("tax").innerText = `$${tax.toFixed(2)}`;
    document.getElementById("grand-total").innerText = `$${grand.toFixed(2)}`;
}


//---------------------------------------------
// CHANGE QUANTITY (+ / -)
//---------------------------------------------
function changeQty(index, amount) {
    cart[index].qty += amount;

    if (cart[index].qty <= 0) {
        cart.splice(index , 1);
    }

    renderCart();
}


//---------------------------------------------
// CHECK INVENTORY LEVELS AFTER SALE
//---------------------------------------------
function checkThresholdAlerts(products) {
    let low = products.filter(p => p.qty <= p.reorder_threshold);

    if (low.length > 0) {
        let msg = low.map(p => `${p.name} (Qty: ${p.qty})`).join("\n");
        alert(" LOW STOCK ALERT:\n\n" + msg);
    }
}


//---------------------------------------------
// COMPLETE SALE (Send to backend)
//---------------------------------------------
async function completeSale() {
    if (cart.length === 0) {
        alert("Cart is empty!");
        return;
    }

    let items = cart.map(i => ({
        product_id: i.product_id,
        qty: i.qty
    }));

    let user_id = localStorage.getItem("user_id");
    let res = await apiPost("/sales/", { cashier_id: user_id, items });

    if (res.error) {
        alert(res.error);
        return;
    }

    alert("Sale completed successfully! Opening receipt...");
    window.open(
        `${API_BASE}/sales/receipt/${res.receipt}?token=${localStorage.getItem("token")}`,
        "_blank"
    );

    cart = [];
    renderCart();
    productsList = await apiGet("/inventory/");
    renderProductList(productsList);
    checkThresholdAlerts(productsList);



    cart = [];
    renderCart();
    productsList = await apiGet("/inventory/");
    renderProductList(productsList);
    checkThresholdAlerts(productsList);
}
