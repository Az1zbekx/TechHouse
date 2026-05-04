import { cartItems, products } from "../data/db.js";
import { v4 as uuidv4 } from "uuid";

export function viewCartItem(req, res) {
    const userId = req.headers["x-user-id"];

    let userCart = cartItems.find(item => item.user_id == userId);

    if (!userCart) {
        userCart = {
            id: uuidv4(),
            user_id: userId,
            products: [],
            quantity: 0
        };
        cartItems.push(userCart);
    }

    const cartWithProducts = {
        ...userCart,
        products: userCart.products.map((item) => {
            const product = products.find(p => p.id === item.product_id);

            return {
                name: product.name,
                price: product.price,
                image_url: product.image_url,
                quantity: item.quantity
            };
        })
    };

    return res.status(200).json(cartWithProducts);
}

export function addToCart(req, res) {
    const userId = req.headers["x-user-id"];
    const { product_id } = req.body;

    const product = products.find(p => p.id === product_id);

    if (!product) {
        return res.status(404).json({ message: "Product not found" });
    }

    if (product.stock = 1){
        return res.status(400).json({ message: "Not enough stock"});
    }
   
    let existing = cartItems.find((itme) => item.user_id == userId);

    if (!existing) {
        existing = {
            id: uuidv4(),
            user_id: userId,
            products: [],
            quantity: 0
        };
        cartItems.push(existing);
    }

    const existingProduct = existing.product.find(
        (item) => item.id == product_id,
    );

    if (existingProduct) {
        existingProduct.quantity = 1;
    } else {
        existing.product.push({
            id: product_id,
            quantity: 1,
        })
    }

    existing.quantity = existing.product.reduce(
        (sum, item) => sum + item.quantity, 0
    );

    return res.status(200).json({message: "Product added to cart"});
}

export function removeCartItem(req, res){};
export function updateCartItem(req, res){};