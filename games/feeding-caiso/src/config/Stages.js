export const STAGES = [
    {
        name: "Morning Dew",
        theme: "Dawn",
        duration: 60,
        backgroundColor: "#E0F7FA",
        atmosphere: {
            overlayColor: "rgba(0, 50, 80, 0.2)", // Cool dawn tint
            windX: 0,
            gravityY: 1.0
        },
        hazards: []
    },
    {
        name: "Sunlit Bloom",
        theme: "Morning",
        duration: 60,
        backgroundColor: "#FFF8E1",
        atmosphere: {
            overlayColor: "rgba(255, 200, 100, 0.1)", // Warm morning
            windX: 0,
            gravityY: 1.0
        },
        hazards: ["bee"]
    },
    {
        name: "Whispering Breeze",
        theme: "Noon",
        duration: 60,
        backgroundColor: "#B3E5FC",
        atmosphere: {
            overlayColor: "rgba(255, 255, 255, 0.0)", // Clear noon
            windX: 2.5, // Strong breeze
            gravityY: 1.0
        },
        hazards: ["wind_gust"]
    },
    {
        name: "Golden Harvest",
        theme: "Afternoon",
        duration: 60,
        backgroundColor: "#FFE0B2",
        atmosphere: {
            overlayColor: "rgba(255, 160, 0, 0.15)", // Golden hour
            windX: 0.5,
            gravityY: 1.0
        },
        hazards: ["leaf"]
    },
    {
        name: "Crimson Sunset",
        theme: "Sunset",
        duration: 60,
        backgroundColor: "#FFCCBC",
        atmosphere: {
            overlayColor: "rgba(200, 50, 0, 0.25)", // Red sunset
            windX: -0.5,
            gravityY: 0.9 // Cooling air, slightly floaty?
        },
        hazards: []
    },
    {
        name: "Twilight Grove",
        theme: "Dusk",
        duration: 60,
        backgroundColor: "#9FA8DA",
        atmosphere: {
            overlayColor: "rgba(20, 0, 60, 0.4)", // Deep purple dusk
            windX: 0,
            gravityY: 1.0
        },
        hazards: ["shadow"]
    },
    {
        name: "Moonlit Lake",
        theme: "Night",
        duration: 60,
        backgroundColor: "#283593",
        atmosphere: {
            overlayColor: "rgba(0, 0, 40, 0.6)", // Dark night
            windX: 0,
            gravityY: 1.0
        },
        hazards: ["ripple"]
    },
    {
        name: "Starry Expanse",
        theme: "Midnight",
        duration: 60,
        backgroundColor: "#1A237E",
        atmosphere: {
            overlayColor: "rgba(0, 0, 20, 0.7)", // Deepest night
            windX: 0,
            gravityY: 0.8 // Lower gravity
        },
        hazards: ["star"]
    },
    {
        name: "Aurora Borealis",
        theme: "Deep Night",
        duration: 60,
        backgroundColor: "#311B92",
        atmosphere: {
            overlayColor: "rgba(0, 255, 100, 0.1)", // Aurora tint
            windX: 5.0, // Magnetic winds?
            gravityY: 0.7
        },
        hazards: ["magnetic_field"]
    },
    {
        name: "Cosmic Dawn",
        theme: "Void",
        duration: 60,
        backgroundColor: "#000000",
        atmosphere: {
            overlayColor: "rgba(100, 0, 100, 0.3)", // Cosmic
            windX: 0,
            gravityY: 0.5 // Very low gravity
        },
        hazards: ["void"]
    }
];
