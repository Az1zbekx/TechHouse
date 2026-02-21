const productsData = [
    {
        id: 1,
        name: "ProStand Mixer 5000",
        description: "Professional grade stand mixer for all your baking needs. Features a powerful 500W motor, 5L stainless steel bowl, and 10 speed settings for perfect mixing every time.",
        price: 299.99,
        category: "Kitchen",
        imageUrl: "https://www.masterhaus.bg/files/products/07/05/05/0705050103-kuhnenski-blender-900-w-styklena-kana-2l-pro-blend-6-hr219500-philips.jpg",
        specifications: {
            "Power": "500W",
            "Capacity": "5L",
            "Speed Settings": "10 speeds",
            "Color": "Silver",
            "Weight": "4.5kg"
        }
    },
    {
        id: 2,
        name: "UltraBlend Pro",
        description: "High-speed blender perfect for smoothies, soups, and more. Powerful 1200W motor with stainless steel blades and 5 preset programs.",
        price: 149.99,
        category: "Kitchen",
        imageUrl: "https://toutici.tn/wp-content/uploads/2025/11/LM962B10.jpg",
        specifications: {
            "Power": "1200W",
            "Blade Material": "Stainless Steel",
            "Programs": "5 presets",
            "Capacity": "1.5L"
        }
    },
    {
        id: 3,
        name: "SmartClean Robot Vacuum",
        description: "Keep your floors spotless with intelligent mapping and powerful suction. App-controlled with 120 minutes of runtime.",
        price: 399.99,
        category: "Cleaning",
        imageUrl: "https://m.media-amazon.com/images/I/61EnsMvyueL.jpg",
        specifications: {
            "Battery Life": "120 mins",
            "Suction Power": "2000Pa",
            "Smart App": "Yes",
            "Noise Level": "55dB"
        }
    },
    {
        id: 4,
        name: "SteamMaster 3000",
        description: "Deep clean your home without chemicals using high-pressure steam. Perfect for floors, carpets, and upholstery.",
        price: 129.99,
        category: "Cleaning",
        imageUrl: "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQGCfeoxgK4WohlQOTv7npBS2kbanaKbsRIfw&s",
        specifications: {
            "Pressure": "4 bar",
            "Tank Capacity": "1.5L",
            "Heat-up Time": "3 mins",
            "Cord Length": "6m"
        }
    },
    {
        id: 5,
        name: "Arctic Breeze AC",
        description: "Portable air conditioner to keep you cool during hot summer days. 12000 BTU with 3 modes and remote control.",
        price: 449.99,
        category: "Heating",
        imageUrl: "https://www.arctic.de/media/3d/2f/15/1583751547/ARCTIC_Breeze_Mobile_G00.jpg",
        specifications: {
            "BTU": "12000",
            "Coverage Area": "400 sq ft",
            "Modes": "Cool/Fan/Dry",
            "Remote Control": "Yes"
        }
    },
    {
        id: 6,
        name: "Ceramic Tower Heater",
        description: "Efficient heating for small to medium sized rooms. Oscillating design with 8-hour timer and remote control.",
        price: 89.99,
        category: "Heating",
        imageUrl: "https://www.honeywellstore.com/store/images/products/large_images/hce323v-digital-ceramic-tower-heater-with-motion-sensor.jpg",
        specifications: {
            "Power": "1500W",
            "Oscillation": "Yes",
            "Timer": "8 hours",
            "Heat Settings": "3 levels"
        }
    },
    {
        id: 7,
        name: "SalonPro Hair Dryer",
        description: "Ionic technology for smooth, frizz-free hair. 2200W professional power with multiple attachments included.",
        price: 79.99,
        category: "Personal",
        imageUrl: "https://images.philips.com/is/image/philipsconsumer/4705ac17035e49ebbe8aae7800c0ae10?$pnglarge$&wid=960",
        specifications: {
            "Power": "2200W",
            "Heat Settings": "3 heat/2 speed",
            "Attachments": "Diffuser included",
            "Technology": "Ionic"
        }
    },
    {
        id: 8,
        name: "HomeHub Smart Speaker",
        description: "Control your smart home and enjoy music with premium 360-degree sound. Built-in voice assistant compatible.",
        price: 99.99,
        category: "Smart",
        imageUrl: "https://i5.walmartimages.com/asr/1ade1557-2879-4303-bf47-c6f529c220e7_1.8edfcf8b0829ea40659a92175bf83b31.jpeg?odnHeight=2000&odnWidth=2000&odnBg=FFFFFF",
        specifications: {
            "Sound": "360 degree",
            "Voice Assistant": "Built-in",
            "Connectivity": "WiFi/Bluetooth",
            "Smart Home": "Compatible"
        }
    },
    {
        id: 9,
        name: "QuickToast Pro",
        description: "4-slice toaster with multiple browning levels and defrost function. Extra-wide slots for bagels and thick bread.",
        price: 59.99,
        category: "Kitchen",
        imageUrl: "https://http2.mlstatic.com/D_NQ_NP_947907-MLA100018706997_122025-O.webp",
        specifications: {
            "Slots": "4 slices",
            "Browning Levels": "7",
            "Functions": "Toast/Defrost/Reheat",
            "Slot Width": "Extra wide"
        }
    },
    {
        id: 10,
        name: "AirPure 500",
        description: "HEPA air purifier for rooms up to 500 sq ft. Removes 99.97% of airborne particles with quiet operation.",
        price: 199.99,
        category: "Smart",
        imageUrl: "https://www.vellepro.com/cdn/shop/files/50006-1.jpg?v=1757936210",
        specifications: {
            "Filter": "True HEPA",
            "Coverage": "500 sq ft",
            "Noise Level": "24dB",
            "Filter Life": "12 months"
        }
    },
    {
        id: 11,
        name: "ChefMaster Microwave",
        description: "1000W microwave with convection and grill functions. Large 30L capacity with smart sensor cooking.",
        price: 179.99,
        category: "Kitchen",
        imageUrl: "https://assets.alexanders-direct.co.uk/media/catalog/product/cache/ba81d38591fbd492e13d5830b945a0fc/c/h/chefmaster_heb643.jpg",
        specifications: {
            "Power": "1000W",
            "Capacity": "30L",
            "Functions": "Microwave/Grill/Convection",
            "Programs": "Auto cook menus"
        }
    },
    {
        id: 12,
        name: "TurboVac Cordless",
        description: "Lightweight cordless vacuum with powerful suction. 45-minute runtime with washable HEPA filter.",
        price: 249.99,
        category: "Cleaning",
        imageUrl: "https://5.imimg.com/data5/SELLER/Default/2025/4/500905000/VC/QR/SG/132024450/61axum-ptgl-sl1500-500x500.jpg",
        specifications: {
            "Runtime": "45 mins",
            "Suction": "150W",
            "Filter": "Washable HEPA",
            "Weight": "2.5kg"
        }
    }
];
