from typing import List, Dict, Any

SEED_CROPS = [
    {
        "name": "Tomato",
        "scientific_name": "Solanum lycopersicum",
        "description": "High-value Solanaceous vegetable crop cultivated globally in open fields and protected polyhouses.",
        "growth_stages": ["Germination", "Seedling", "Vegetative", "Flowering", "Fruit Set", "Ripening"],
        "common_diseases": ["Tomato Early Blight", "Tomato Late Blight", "Septoria Leaf Spot", "Bacterial Canker"],
        "common_pests": ["Whitefly", "Tomato Hornworm", "Aphids", "Fruit Borer"]
    },
    {
        "name": "Potato",
        "scientific_name": "Solanum tuberosum",
        "description": "Major tuber staple crop susceptible to foliar fungal and oomycete pathogens.",
        "growth_stages": ["Sprout Development", "Vegetative Growth", "Tuber Initiation", "Tuber Bulking", "Maturation"],
        "common_diseases": ["Potato Late Blight", "Potato Early Blight", "Blackleg", "Common Scab"],
        "common_pests": ["Colorado Potato Beetle", "Potato Tuber Moth", "Aphids"]
    },
    {
        "name": "Wheat",
        "scientific_name": "Triticum aestivum",
        "description": "Principal cereal grain grown across temperate and subtropical agricultural belts.",
        "growth_stages": ["Tillering", "Stem Elongation", "Booting", "Heading", "Flowering", "Milking", "Dough Stage", "Ripening"],
        "common_diseases": ["Stripe (Yellow) Rust", "Leaf Rust", "Powdery Mildew", "Loose Smut"],
        "common_pests": ["Wheat Aphid", "Armyworm", "Termites"]
    },
    {
        "name": "Rice",
        "scientific_name": "Oryza sativa",
        "description": "Primary dietary staple for more than half the global population grown under flooded and upland ecosystems.",
        "growth_stages": ["Seedling", "Tillering", "Panicle Initiation", "Booting", "Heading", "Flowering", "Grain Filling", "Maturation"],
        "common_diseases": ["Bacterial Leaf Blight", "Rice Blast", "Sheath Blight", "Brown Spot"],
        "common_pests": ["Brown Planthopper", "Stem Borer", "Leaf Folder", "Gall Midge"]
    },
    {
        "name": "Maize",
        "scientific_name": "Zea mays",
        "description": "Versatile cereal utilized extensively for food, animal feed, and industrial starches.",
        "growth_stages": ["Emergence (VE)", "Vegetative (V1-V12)", "Tasseling (VT)", "Silking (R1)", "Blister (R2)", "Milk (R3)", "Dough (R4)", "Dent (R5)", "Maturity (R6)"],
        "common_diseases": ["Common Rust", "Northern Corn Leaf Blight", "Maize Smut"],
        "common_pests": ["Fall Armyworm", "Stem Borer", "Corn Earworm"]
    },
    {
        "name": "Cotton",
        "scientific_name": "Gossypium hirsutum",
        "description": "Premier natural fiber cash crop demanding strict pest and moisture management.",
        "growth_stages": ["Emergence", "Squaring", "Flowering", "Boll Development", "Boll Opening"],
        "common_diseases": ["Bacterial Blight", "Leaf Curl Virus", "Alternaria Leaf Spot"],
        "common_pests": ["Pink Bollworm", "Whitefly", "Thrips", "Jassids"]
    },
    {
        "name": "Apple",
        "scientific_name": "Malus domestica",
        "description": "High-latitude and mountainous temperate deciduous fruit tree crop.",
        "growth_stages": ["Dormant", "Silver Tip", "Green Tip", "Tight Cluster", "Pink", "Bloom", "Petal Fall", "Fruit Development"],
        "common_diseases": ["Apple Scab", "Powdery Mildew", "Cedar Apple Rust", "Fire Blight"],
        "common_pests": ["Codling Moth", "San Jose Scale", "Apple Maggot"]
    }
]

SEED_DISEASES = [
    {
        "crop_name": "Tomato",
        "name": "Tomato Early Blight",
        "scientific_name": "Alternaria solani",
        "description": "Destructive fungal disease affecting tomato foliage, stems, and fruit throughout the growing season.",
        "symptoms": [
            "Dark brown circular lesions with distinctive concentric rings (target board pattern)",
            "Yellow chlorotic halos surrounding lesions on older foliage",
            "Defoliation starting from lower canopy moving upward"
        ],
        "causes": ["Alternaria solani fungal spores", "Frequent rain, heavy dew, warm temperatures (24-29°C)"],
        "risk_factors": ["Overhead sprinkler irrigation", "Dense canopy with poor airflow", "Stressed plants with low nitrogen"],
        "severity_levels": {
            "LOW": "A few isolated lesions on bottom leaves (<5% leaf area affected)",
            "MODERATE": "Concentric spots spreading to middle foliage (15-30% leaf area affected)",
            "HIGH": "Extensive defoliation with lesions spreading to stems and green fruit (>40% canopy damaged)"
        },
        "prevention": [
            "Plant certified pathogen-free seeds and resistant varieties",
            "Maintain 60-90cm row spacing to facilitate air circulation",
            "Apply organic mulch around plant bases to prevent soil splash"
        ],
        "management": [
            "Prune off infected lower leaves and safely dispose outside the farm",
            "Transition to drip irrigation systems",
            "Apply copper-based fungicides or bio-fungicides per local extension schedules"
        ],
        "image_examples": []
    },
    {
        "crop_name": "Tomato",
        "name": "Tomato Late Blight",
        "scientific_name": "Phytophthora infestans",
        "description": "Rapidly spreading oomycete disease that can destroy entire tomato canopies within days in cool wet weather.",
        "symptoms": [
            "Water-soaked dark green to brownish lesions expanding rapidly",
            "White velvety fungal growth on the underside of infected leaves in humid mornings",
            "Firm brown leathery decay on developing fruit"
        ],
        "causes": ["Phytophthora infestans", "Cool temperatures (15-22°C) combined with sustained relative humidity >90%"],
        "risk_factors": ["Protracted rainy spells", "Cool dewy nights", "Proximity to infected potato fields"],
        "severity_levels": {
            "LOW": "Early water-soaked lesions detected on isolated leaves",
            "MODERATE": "Foliar lesions on multiple plants with visible sporulation",
            "HIGH": "Widespread stem collapse and fruit decay requiring urgent quarantine"
        },
        "prevention": [
            "Scout fields twice weekly during cool moist weather periods",
            "Eliminate volunteer tomato and potato cull piles",
            "Ensure full sun exposure and well-drained field orientation"
        ],
        "management": [
            "Remove and destroy infected plants immediately",
            "Apply approved protectant fungicides before rain events"
        ],
        "image_examples": []
    },
    {
        "crop_name": "Wheat",
        "name": "Wheat Stripe (Yellow) Rust",
        "scientific_name": "Puccinia striiformis",
        "description": "High-risk airborne foliar disease causing linear stripes of yellow-orange fungal pustules.",
        "symptoms": [
            "Bright yellow-orange powdery pustules arranged in parallel lines along leaf veins",
            "Premature desiccation of flag leaves during grain filling",
            "Severe reduction in photosynthetic capacity leading to shriveled grains"
        ],
        "causes": ["Puccinia striiformis fungal urediniospores carried long distances by wind"],
        "risk_factors": ["Cool spring temperatures (10-18°C)", "High relative humidity and heavy morning dew"],
        "severity_levels": {
            "LOW": "Trace pustules on lower leaves",
            "MODERATE": "Stripes expanding up to penultimate leaf",
            "HIGH": "Flag leaf completely colonized by rust pustules"
        },
        "prevention": ["Sow rust-resistant wheat varieties (Yr genes)", "Avoid excessive early nitrogen application"],
        "management": ["Timely application of recommended triazole fungicides at first sign of rust on flag leaf"],
        "image_examples": []
    },
    {
        "crop_name": "Rice",
        "name": "Rice Bacterial Leaf Blight",
        "scientific_name": "Xanthomonas oryzae pv. oryzae",
        "description": "Severe vascular bacterial disease causing leaf wilting and bleaching along leaf edges.",
        "symptoms": [
            "Water-soaked to yellowish wavy lesions starting at leaf tips and advancing along leaf margins",
            "Milky bacterial ooze droplets on young lesions in humid mornings",
            "Leaves turn grayish-white and dry up completely (kresek phase)"
        ],
        "causes": ["Xanthomonas oryzae bacterium entering through natural openings and wounds"],
        "risk_factors": ["High winds, rainstorms, and typhoons causing foliar abrasion", "Flooding and excess nitrogen"],
        "severity_levels": {
            "LOW": "Tip lesions on <10% of leaves",
            "MODERATE": "Wavy margin lesions covering 25-50% of canopy",
            "HIGH": "Severe foliar blight with lodging risk"
        },
        "prevention": ["Cultivate resistant rice lines", "Balance fertilizer with adequate potassium"],
        "management": ["Drain flooded paddies temporarily", "Avoid mechanical field entry during wet morning hours"],
        "image_examples": []
    }
]

SEED_PESTS = [
    {
        "crop_name": "Tomato",
        "name": "Tomato Whitefly Infestation",
        "scientific_name": "Bemisia tabaci",
        "description": "Tiny sap-sucking insect vector responsible for transmitting debilitating viral pathogens like Tomato Yellow Leaf Curl Virus.",
        "symptoms": [
            "Small yellowish-white winged adults fluttering when plants are disturbed",
            "Excretion of clear sticky honeydew attracting black sooty mold fungus",
            "Chlorotic leaf speckling, leaf cupping, and reduced fruit vigor"
        ],
        "damage_description": "Direct phloem sap feeding weakens plants; secondary viral transmission causes complete fruit abortion.",
        "risk_factors": ["Hot, dry microclimates", "Continuous Solanaceous cropping", "Absence of natural predators"],
        "prevention": [
            "Install 50-mesh insect-proof netting in nursery houses",
            "Hang yellow sticky cards (1 per 100 sq meters) for early detection",
            "Intercrop with aromatic repellents like marigold or basil"
        ],
        "management": [
            "Spray certified neem oil or potassium soap solutions to smother nymphs",
            "Release parasitoid wasps (Encarsia formosa) in greenhouse setups"
        ],
        "image_examples": []
    },
    {
        "crop_name": "Maize",
        "name": "Maize Fall Armyworm Infestation",
        "scientific_name": "Spodoptera frugiperda",
        "description": "Aggressive, polyphagous invasive caterpillar that devastates maize whorls and emerging reproductive ears.",
        "symptoms": [
            "Ragged 'window-pane' holes on young leaves",
            "Coarse yellowish-brown sawdust-like frass accumulating inside the central leaf whorl",
            "Severed central shoots ('dead heart') in young maize"
        ],
        "damage_description": "Larvae consume leaf tissue voraciously and bore directly into developing cobs.",
        "risk_factors": ["Warm tropical/subtropical nights", "Late planting dates", "Staggered regional plantings"],
        "prevention": [
            "Adopt early synchronized regional planting",
            "Intercrop maize with companion legumes (Push-Pull strategy with Desmodium and Napier grass)"
        ],
        "management": [
            "Hand-pick egg masses and caterpillars in smallholdings",
            "Apply bio-pesticides like Bacillus thuringiensis (Bt) or Spinosad into the central leaf whorl"
        ],
        "image_examples": []
    },
    {
        "crop_name": "Cotton",
        "name": "Cotton Pink Bollworm Infestation",
        "scientific_name": "Pectinophora gossypiella",
        "description": "Major economic pest whose larvae burrow into cotton squares and bolls, destroying fiber quality and seed viability.",
        "symptoms": [
            "Rosetted flowers that twist and fail to open normally",
            "Small entrance pinholes in developing green bolls sealed by frass",
            "Stained, discolored lint and hollowed-out seeds"
        ],
        "damage_description": "Internal boll feeding destroys lint fibers, drops boll weight, and introduces boll rot fungi.",
        "risk_factors": ["Ratoon cotton crops", "Late harvest and delayed crop stalk destruction"],
        "prevention": [
            "Deploy pheromone delta traps (5 traps/hectare) for monitoring adult moth emergence",
            "Observe a strict cotton-free closed season of at least 90 days"
        ],
        "management": [
            "Implement mating disruption pheromone dispensers",
            "Shred and deep-plow cotton crop residues immediately post-harvest"
        ],
        "image_examples": []
    }
]
