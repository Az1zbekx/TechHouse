import express from 'express';
import {viewCartItem, addToCart, updateCartItem, removeCartItem} from "../controllers/cartController.js";
const router = express.Router();

router.get('/', viewCartItem);
router.post('/', addToCart);
router.put('/:id', updateCartItem);
router.delete('/:id', removeCartItem);

export default router;
