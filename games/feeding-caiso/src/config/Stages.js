// Phase 6: The Hollow Deep - 10 Stage Configuration
// Hollow Knight-inspired underground kingdom theme
export const STAGES = [
    // Stage 1: The Forgotten Crossroads
    {
        name: "The Forgotten Crossroads",
        nameKo: "잊혀진 교차로",
        theme: "crossroads",
        duration: 60000,
        backgroundColor: "#1a1a2e",
        atmosphere: {
            overlayColor: "rgba(15, 15, 27, 0.3)",
            windX: 0,
            gravityY: 1.0
        },
        lighting: {
            ambientLight: 0.3,
            playerLightRadius: 150,
            playerLightColor: "rgba(116, 185, 255, 0.4)",
            fixedLights: [],
            bloom: false,
            vignette: true
        },
        parallax: {
            layers: [
                { key: "bg_crossroads_far",  speed: 0.1, y: 0,   height: 854 },
                { key: "bg_crossroads_mid",  speed: 0.3, y: 200, height: 400 },
                { key: "bg_crossroads_near", speed: 0.6, y: 500, height: 354 }
            ]
        },
        particles: {
            emitters: [
                { type: "dust", density: "low", color: "#636e72", sizeRange: [2, 5] }
            ]
        },
        gameplay: {
            hazards: [],
            itemSpeedMult: 1.0,
            scoreMultiplier: 1.0,
            slipperyFloor: false,
            visibilityRadius: null,
            windDirection: "static"
        },
        audio: {
            bgmKey: "bgm_crossroads",
            ambience: ["drip", "wind_light"],
            reverbLevel: 0.3
        }
    },
    // Stage 2: Greenpath
    {
        name: "Greenpath",
        nameKo: "녹색 거리",
        theme: "greenpath",
        duration: 60000,
        backgroundColor: "#1a3a2e",
        atmosphere: {
            overlayColor: "rgba(20, 60, 40, 0.25)",
            windX: 0.5,
            gravityY: 1.0
        },
        lighting: {
            ambientLight: 0.35,
            playerLightRadius: 140,
            playerLightColor: "rgba(116, 185, 255, 0.4)",
            accentLightColor: "rgba(46, 204, 113, 0.2)",
            fixedLights: [],
            bloom: false,
            vignette: true
        },
        parallax: {
            layers: [
                { key: "bg_greenpath_far",  speed: 0.1, y: 0,   height: 854 },
                { key: "bg_greenpath_mid",  speed: 0.3, y: 200, height: 400 },
                { key: "bg_greenpath_near", speed: 0.6, y: 500, height: 354 }
            ]
        },
        particles: {
            emitters: [
                { type: "spore", density: "low", color: "#2ecc71", sizeRange: [3, 8] }
            ]
        },
        gameplay: {
            hazards: ["acid_drop"],
            itemSpeedMult: 1.1,
            scoreMultiplier: 1.0,
            slipperyFloor: false,
            visibilityRadius: null,
            windDirection: "static"
        },
        audio: {
            bgmKey: "bgm_greenpath",
            ambience: ["insects", "water_flow"],
            reverbLevel: 0.3
        }
    },
    // Stage 3: Fungal Wastes
    {
        name: "Fungal Wastes",
        nameKo: "곰팡이 황무지",
        theme: "fungal",
        duration: 60000,
        backgroundColor: "#2d1b4e",
        atmosphere: {
            overlayColor: "rgba(50, 20, 80, 0.35)",
            windX: 0,
            gravityY: 0.9
        },
        lighting: {
            ambientLight: 0.25,
            playerLightRadius: 130,
            playerLightColor: "rgba(116, 185, 255, 0.4)",
            fixedLights: [
                { x: 120, y: 400, radius: 80, color: "rgba(162, 155, 254, 0.3)" },
                { x: 360, y: 300, radius: 60, color: "rgba(162, 155, 254, 0.25)" }
            ],
            bloom: false,
            vignette: true
        },
        parallax: {
            layers: [
                { key: "bg_fungal_far",  speed: 0.1, y: 0,   height: 854 },
                { key: "bg_fungal_mid",  speed: 0.3, y: 200, height: 400 },
                { key: "bg_fungal_near", speed: 0.6, y: 500, height: 354 }
            ]
        },
        particles: {
            emitters: [
                { type: "spore", density: "high", color: "#a29bfe", sizeRange: [8, 20], alpha: 0.4 }
            ]
        },
        gameplay: {
            hazards: ["exploding_spore"],
            itemSpeedMult: 1.2,
            scoreMultiplier: 1.0,
            slipperyFloor: false,
            visibilityRadius: null,
            windDirection: "static"
        },
        audio: {
            bgmKey: "bgm_fungal",
            ambience: ["spore_pop", "mushroom_hum"],
            reverbLevel: 0.5
        }
    },
    // Stage 4: City of Tears
    {
        name: "City of Tears",
        nameKo: "눈물의 도시",
        theme: "city",
        duration: 60000,
        backgroundColor: "#1a2a4a",
        atmosphere: {
            overlayColor: "rgba(20, 40, 80, 0.4)",
            windX: 1.0,
            gravityY: 1.1
        },
        lighting: {
            ambientLight: 0.3,
            playerLightRadius: 140,
            playerLightColor: "rgba(116, 185, 255, 0.35)",
            fixedLights: [
                { x: 100, y: 350, radius: 50, color: "rgba(255, 200, 100, 0.4)" },
                { x: 250, y: 280, radius: 40, color: "rgba(255, 200, 100, 0.3)" },
                { x: 380, y: 320, radius: 45, color: "rgba(255, 200, 100, 0.35)" }
            ],
            bloom: false,
            vignette: true
        },
        parallax: {
            layers: [
                { key: "bg_city_far",  speed: 0.1, y: 0,   height: 854 },
                { key: "bg_city_mid",  speed: 0.3, y: 150, height: 500 },
                { key: "bg_city_near", speed: 0.6, y: 500, height: 354 }
            ]
        },
        particles: {
            emitters: [
                { type: "rain", density: "very_high", color: "rgba(150, 180, 220, 0.5)", sizeRange: [1, 2] }
            ]
        },
        gameplay: {
            hazards: ["rain_gust"],
            itemSpeedMult: 1.3,
            scoreMultiplier: 1.0,
            slipperyFloor: true,
            visibilityRadius: null,
            windDirection: "static"
        },
        audio: {
            bgmKey: "bgm_city",
            ambience: ["rain_heavy", "distant_bell"],
            reverbLevel: 0.7
        }
    },
    // Stage 5: Crystal Peak
    {
        name: "Crystal Peak",
        nameKo: "수정 봉우리",
        theme: "crystal",
        duration: 60000,
        backgroundColor: "#2a1a3a",
        atmosphere: {
            overlayColor: "rgba(50, 30, 70, 0.2)",
            windX: 0,
            gravityY: 1.0
        },
        lighting: {
            ambientLight: 0.4,
            playerLightRadius: 160,
            playerLightColor: "rgba(230, 150, 255, 0.4)",
            fixedLights: [
                { x: 200, y: 250, radius: 100, color: "rgba(230, 150, 255, 0.3)" },
                { x: 400, y: 450, radius: 70, color: "rgba(230, 150, 255, 0.25)" }
            ],
            bloom: true,
            vignette: true
        },
        parallax: {
            layers: [
                { key: "bg_crystal_far",  speed: 0.1, y: 0,   height: 854 },
                { key: "bg_crystal_mid",  speed: 0.3, y: 200, height: 400 },
                { key: "bg_crystal_near", speed: 0.6, y: 500, height: 354 }
            ]
        },
        particles: {
            emitters: [
                { type: "dust", density: "medium", color: "#dfe6e9", sizeRange: [2, 4] }
            ]
        },
        gameplay: {
            hazards: ["crystal_beam"],
            itemSpeedMult: 1.4,
            scoreMultiplier: 1.0,
            slipperyFloor: false,
            visibilityRadius: null,
            windDirection: "static"
        },
        audio: {
            bgmKey: "bgm_crystal",
            ambience: ["crystal_chime", "drill_distant"],
            reverbLevel: 0.6
        }
    },
    // Stage 6: Deepnest
    {
        name: "Deepnest",
        nameKo: "깊은 둥지",
        theme: "deepnest",
        duration: 60000,
        backgroundColor: "#0a0a0f",
        atmosphere: {
            overlayColor: "rgba(0, 0, 0, 0.85)",
            windX: 0,
            gravityY: 1.0
        },
        lighting: {
            ambientLight: 0.05,
            playerLightRadius: 100,
            playerLightColor: "rgba(255, 200, 150, 0.6)",
            fixedLights: [],
            bloom: false,
            vignette: true
        },
        parallax: {
            layers: [
                { key: "bg_deepnest_far", speed: 0.05, y: 0, height: 854 }
            ]
        },
        particles: {
            emitters: []
        },
        gameplay: {
            hazards: ["mimic"],
            itemSpeedMult: 1.3,
            scoreMultiplier: 1.0,
            slipperyFloor: false,
            visibilityRadius: 100,
            windDirection: "static"
        },
        audio: {
            bgmKey: "bgm_deepnest",
            ambience: ["skitter", "drip_echo"],
            reverbLevel: 0.8
        }
    },
    // Stage 7: Kingdom's Edge
    {
        name: "Kingdom's Edge",
        nameKo: "왕국의 끝자락",
        theme: "edge",
        duration: 60000,
        backgroundColor: "#1a1a20",
        atmosphere: {
            overlayColor: "rgba(30, 30, 35, 0.3)",
            windX: 3.0,
            gravityY: 0.9
        },
        lighting: {
            ambientLight: 0.35,
            playerLightRadius: 150,
            playerLightColor: "rgba(200, 200, 220, 0.3)",
            fixedLights: [],
            bloom: false,
            vignette: true,
            topGradient: { color: "rgba(200, 200, 220, 0.15)", height: 200 }
        },
        parallax: {
            layers: [
                { key: "bg_edge_far",  speed: 0.1, y: 0,   height: 854 },
                { key: "bg_edge_mid",  speed: 0.3, y: 200, height: 400 },
                { key: "bg_edge_near", speed: 0.6, y: 500, height: 354 }
            ]
        },
        particles: {
            emitters: [
                { type: "ash", density: "very_high", color: "#dfe6e9", sizeRange: [3, 6] }
            ]
        },
        gameplay: {
            hazards: ["ash_gust"],
            itemSpeedMult: 1.5,
            scoreMultiplier: 1.0,
            slipperyFloor: false,
            visibilityRadius: null,
            windDirection: "alternating",
            windAlternateInterval: 5000
        },
        audio: {
            bgmKey: "bgm_edge",
            ambience: ["wind_howl", "distant_cry"],
            reverbLevel: 0.5
        }
    },
    // Stage 8: The Abyss
    {
        name: "The Abyss",
        nameKo: "심연",
        theme: "abyss",
        duration: 60000,
        backgroundColor: "#050508",
        atmosphere: {
            overlayColor: "rgba(5, 0, 15, 0.7)",
            windX: 0,
            gravityY: 0.7
        },
        lighting: {
            ambientLight: 0.1,
            playerLightRadius: 120,
            playerLightColor: "rgba(162, 155, 254, 0.4)",
            fixedLights: [],
            bloom: false,
            vignette: true
        },
        parallax: {
            layers: [
                { key: "bg_abyss_far", speed: 0.05, y: 0, height: 854 }
            ]
        },
        particles: {
            emitters: [
                { type: "void", density: "medium", color: "#a29bfe", sizeRange: [3, 8] }
            ]
        },
        gameplay: {
            hazards: ["void_tendril"],
            itemSpeedMult: 1.4,
            scoreMultiplier: 1.0,
            slipperyFloor: false,
            visibilityRadius: null,
            windDirection: "static",
            voidRising: true,
            voidRisingStart: 40000
        },
        audio: {
            bgmKey: "bgm_abyss",
            ambience: ["void_hum", "heartbeat"],
            reverbLevel: 0.9
        }
    },
    // Stage 9: White Palace
    {
        name: "White Palace",
        nameKo: "백색 궁전",
        theme: "palace",
        duration: 60000,
        backgroundColor: "#e8e8f0",
        atmosphere: {
            overlayColor: "rgba(240, 240, 250, 0.1)",
            windX: 0,
            gravityY: 1.0
        },
        lighting: {
            ambientLight: 0.8,
            playerLightRadius: 200,
            playerLightColor: "rgba(255, 255, 255, 0.2)",
            fixedLights: [],
            bloom: true,
            vignette: false,
            playerShadow: true
        },
        parallax: {
            layers: [
                { key: "bg_palace_far",  speed: 0.1, y: 0,   height: 854 },
                { key: "bg_palace_mid",  speed: 0.3, y: 200, height: 400 },
                { key: "bg_palace_near", speed: 0.6, y: 500, height: 354 }
            ]
        },
        particles: {
            emitters: [
                { type: "dust", density: "medium", color: "#b2bec3", sizeRange: [2, 4] }
            ]
        },
        gameplay: {
            hazards: ["buzzsaw"],
            itemSpeedMult: 1.6,
            scoreMultiplier: 2.0,
            slipperyFloor: false,
            visibilityRadius: null,
            windDirection: "static"
        },
        audio: {
            bgmKey: "bgm_palace",
            ambience: ["gear_grind", "metal_ring"],
            reverbLevel: 0.4
        }
    },
    // Stage 10: The Radiance
    {
        name: "The Radiance",
        nameKo: "광휘",
        theme: "radiance",
        duration: 90000,
        backgroundColor: "#3a2000",
        atmosphere: {
            overlayColor: "rgba(255, 150, 0, 0.15)",
            windX: 0,
            gravityY: 0.5
        },
        lighting: {
            ambientLight: 0.5,
            playerLightRadius: 180,
            playerLightColor: "rgba(255, 200, 100, 0.4)",
            fixedLights: [
                { x: 240, y: 100, radius: 300, color: "rgba(255, 180, 50, 0.3)" }
            ],
            bloom: true,
            vignette: false,
            ambientLightRamp: { from: 0.5, to: 0.9 }
        },
        parallax: {
            layers: [
                { key: "bg_radiance_far",  speed: 0.1, y: 0,   height: 854, autoScroll: 0.5 },
                { key: "bg_radiance_mid",  speed: 0.3, y: 150, height: 500, autoScroll: 0.3 }
            ]
        },
        particles: {
            emitters: [
                { type: "spore", density: "extreme", color: "#ff9500", sizeRange: [4, 12] }
            ]
        },
        gameplay: {
            hazards: ["infection_rain", "light_beam"],
            itemSpeedMult: 1.8,
            scoreMultiplier: 3.0,
            slipperyFloor: false,
            visibilityRadius: null,
            windDirection: "random",
            windRandomRange: [-2, 2]
        },
        audio: {
            bgmKey: "bgm_radiance",
            ambience: ["infection_pulse", "organ_swell"],
            reverbLevel: 0.6
        }
    }
];
