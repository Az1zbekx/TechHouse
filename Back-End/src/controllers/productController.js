import { products  } from "../data/db.js";
import { v4 as uuidv4 } from 'uuid';

export function listProducts(req, res) {
    return res.status(200).json({products});
};

export function getSingleProduct(req, res) {
    const id = req.params.id
    const product = products.find(product => product.id == id);

    if(!product) {
        return res.status(404).json({
            message: "Product not found"
        });
    };

    return res.status(200).json({product})
};

export function deleteProduct(req, res) {
    const id = req.params.id
    const product = products.find(product => product.id == id);

    if(!product) {
        return res.status(404).json({
            message: "Product not found"
        });
    };

    const productIndex = products.findIndex(product => product.id == id)
    products.splice(productIndex, 1)

    return res.status(200).json({
        message: "Product deleted successfully!"
    });
};

export function updateProduct(req, res) {
    const id = req.params.id
    const product = products.find(product => product.id == id);

    if(!product) {
        return res.status(404).json({
            message: "Product not found"
        });
    };

    const{name, description, price, stock, category} = req.body;
    
    if(!name || !description || !price || !stock  || !category){
        return res.status(400).json({message: "New product are required"})
    }

    product.name = name ??  product.name
    product.description = description ?? product.description
    product.price = price ?? product.price 
    product.stock = stock ?? product.stock
    product.category = category ?? product.category
    product.updated_at = Date()

    return res.status(200).json({message: "Product elements updeted successfully!"});

};

export function createProduct(req, res) {
    const{name, description, price, stock, category} = req.body;

    if(!name || !description || !price || !stock  || !category){
        return res.status(400).json({message: "New product are required"})
    }

    const newProduct =  {
        id: uuidv4(),
        name,
        description,
        price,
        stock,
        category,
        create_at: Date(),
        updated_at: Date()
    }

    products.push(newProduct);

    return res.status(200).json({message: "New product created successfully!"});
};
