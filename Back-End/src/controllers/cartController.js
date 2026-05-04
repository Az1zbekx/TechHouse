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
                ...product,
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

    let userCart = cartItems.find(item => item.user_id == userId);

    if (!userCart) {
        userCart = {
            id: uuidv4(),
            user_id: userId,
            products: [],
        };
        cartItems.push(userCart);
    }

    const existingItem = userCart.products.find(p => p.product_id === product_id);

    if (existingItem) {
        existingItem.quantity += 1;
    } else {
        userCart.products.push({
            product_id,
            quantity: 1
        });
    }

    res.json(userCart);
}