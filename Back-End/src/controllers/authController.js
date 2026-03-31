import user from "../data/db.js";
import generateId from "../utils/generateId.js";
import bcrypt from "bcrypt"

export function register() {
    console.log(`Checking request body ${req.body}`);

    const { username, email, password} = req.body

    if (!username || !email || !password){
        return res.status(400).json({
            message: "Username, email and password are required"
        })
    }

    const passwordHash = bcrypt.hash(password, 10)
    const user = {
        id: generateId(users),
        username,
        email,
        password
    }

    console.log(`User info ${username} ${email} ${password}`);
}

export function login() {}
