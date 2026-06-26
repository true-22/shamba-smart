"""
Treatment Recommendations Database
=====================================
Maps every PlantVillage disease class to practical treatment advice
tailored for small-scale farmers in Kenya.

Structure per entry:
  - disease       : human-readable display name
  - crop          : affected crop
  - severity      : low / medium / high
  - symptoms      : brief visual description
  - organic       : low-cost organic remedy (accessible in rural Kenya)
  - chemical      : approved agrochemical (available via agrovets)
  - prevention    : cultural practices
  - urgency       : how quickly to act
  - local_tip     : Kenya-specific advice
"""

TREATMENTS = {
    # ── BACKGROUND / NO PLANT ─────────────────────────────────────────
    "Background_without_leaves": {
        "disease"    : "No Plant Detected",
        "crop"       : "Unknown",
        "severity"   : "none",
        "symptoms"   : "No leaf or plant material detected in this image.",
        "organic"    : "N/A",
        "chemical"   : "N/A",
        "prevention" : "Point your camera directly at a single leaf, filling the frame.",
        "urgency"    : "None — please retake the photo.",
        "local_tip"  : "Hold the camera 15–20cm from one leaf, in good daylight, with the leaf filling the frame.",
    },
    # ── APPLE ────────────────────────────────────────────────────
    "Apple___Apple_scab": {
        "disease"    : "Apple Scab",
        "crop"       : "Apple",
        "severity"   : "medium",
        "symptoms"   : "Olive-green to brown scab-like lesions on leaves and fruit.",
        "organic"    : "Apply 1 tbsp baking soda + 1 tsp neem oil in 1L water. Spray every 7 days.",
        "chemical"   : "Captan or Mancozeb fungicide (follow label instructions). Available at agrovets.",
        "prevention" : "Prune for airflow. Remove fallen leaves. Avoid overhead irrigation.",
        "urgency"    : "Treat within 3–5 days to prevent spreading.",
        "local_tip"  : "Burn or bury infected leaves — do NOT compost them.",
    },
    "Apple___Black_rot": {
        "disease"    : "Apple Black Rot",
        "crop"       : "Apple",
        "severity"   : "high",
        "symptoms"   : "Brown circular leaf spots with purple borders. Black rotting fruit.",
        "organic"    : "Remove infected branches immediately. Spray copper-based fungicide.",
        "chemical"   : "Thiophanate-methyl or Captan. Apply every 10–14 days.",
        "prevention" : "Remove mummified fruit. Prune dead wood. Space trees for airflow.",
        "urgency"    : "Act immediately — spreads rapidly in wet weather.",
        "local_tip"  : "During long rains, inspect weekly and remove infected material.",
    },
    "Apple___Cedar_apple_rust": {
        "disease"    : "Cedar Apple Rust",
        "crop"       : "Apple",
        "severity"   : "medium",
        "symptoms"   : "Bright orange-yellow spots on upper leaf surface.",
        "organic"    : "Neem oil spray (2%) every 7 days during early infection.",
        "chemical"   : "Myclobutanil (Eagle 40WP) fungicide at first sign of symptoms.",
        "prevention" : "Plant rust-resistant apple varieties. Remove nearby cedar/juniper trees.",
        "urgency"    : "Treat within 1 week of first symptoms.",
        "local_tip"  : "This disease requires two host plants. Removing junipers nearby helps.",
    },
    "Apple___healthy": {
        "disease"    : "Healthy Apple",
        "crop"       : "Apple",
        "severity"   : "none",
        "symptoms"   : "No disease detected. Plant appears healthy.",
        "organic"    : "Continue current care routine.",
        "chemical"   : "No treatment needed.",
        "prevention" : "Regular inspection, proper spacing, balanced fertiliser.",
        "urgency"    : "None — keep monitoring weekly.",
        "local_tip"  : "Healthy plants need good soil nutrition. Add organic compost seasonally.",
    },

    # ── BLUEBERRY ────────────────────────────────────────────────
    "Blueberry___healthy": {
        "disease"    : "Healthy Blueberry",
        "crop"       : "Blueberry",
        "severity"   : "none",
        "symptoms"   : "No disease detected.",
        "organic"    : "Maintain acidic soil (pH 4.5–5.5) with organic matter.",
        "chemical"   : "No treatment needed.",
        "prevention" : "Mulch with pine needles. Water at base to keep leaves dry.",
        "urgency"    : "None.",
        "local_tip"  : "Blueberries prefer cooler highland conditions in Kenya.",
    },

    # ── CHERRY ───────────────────────────────────────────────────
    "Cherry_(including_sour)___Powdery_mildew": {
        "disease"    : "Cherry Powdery Mildew",
        "crop"       : "Cherry",
        "severity"   : "medium",
        "symptoms"   : "White powdery coating on leaves and young shoots.",
        "organic"    : "Mix 1 tbsp baking soda + 1 tsp dish soap in 1L water. Spray leaves.",
        "chemical"   : "Sulfur-based fungicide or Triadimefon. Apply every 10 days.",
        "prevention" : "Improve air circulation. Avoid excess nitrogen fertiliser.",
        "urgency"    : "Treat within 1 week. Spreads fast in dry weather.",
        "local_tip"  : "Common in dry highland areas. More frequent in Feb–March.",
    },
    "Cherry_(including_sour)___healthy": {
        "disease"    : "Healthy Cherry",
        "crop"       : "Cherry",
        "severity"   : "none",
        "symptoms"   : "No disease detected.",
        "organic"    : "Continue regular care.",
        "chemical"   : "No treatment needed.",
        "prevention" : "Prune annually for airflow.",
        "urgency"    : "None.",
        "local_tip"  : "Cherry grows well in Kenyan highlands above 1,800m.",
    },

    # ── CORN (MAIZE) ─────────────────────────────────────────────
    "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot": {
        "disease"    : "Maize Gray Leaf Spot",
        "crop"       : "Maize",
        "severity"   : "high",
        "symptoms"   : "Grey-tan rectangular lesions running along leaf veins.",
        "organic"    : "Neem oil spray (3%) every 7–10 days. Remove heavily infected leaves.",
        "chemical"   : "Strobilurin fungicide (e.g., Amistar/Azoxystrobin). Spray at tasseling.",
        "prevention" : "Use certified resistant maize seeds (e.g., DK8031, H614D). Crop rotation.",
        "urgency"    : "High — can reduce yield by 50% if untreated. Act within 3 days.",
        "local_tip"  : "Very common in western Kenya. Ask your agrovet for certified GLS-resistant seeds.",
    },
    "Corn_(maize)___Common_rust_": {
        "disease"    : "Maize Common Rust",
        "crop"       : "Maize",
        "severity"   : "medium",
        "symptoms"   : "Orange-red powdery pustules on both leaf surfaces.",
        "organic"    : "Remove infected lower leaves. Apply neem oil spray as preventive.",
        "chemical"   : "Mancozeb or Propiconazole fungicide. Apply early morning.",
        "prevention" : "Plant rust-tolerant varieties. Early planting avoids peak rust season.",
        "urgency"    : "Treat within 5 days. Spreads quickly in cool, humid conditions.",
        "local_tip"  : "Common in Rift Valley & Central Kenya highlands. Monitor during long rains.",
    },
    "Corn_(maize)___Northern_Leaf_Blight": {
        "disease"    : "Maize Northern Leaf Blight",
        "crop"       : "Maize",
        "severity"   : "high",
        "symptoms"   : "Long (5–15cm) tan-brown cigar-shaped lesions on leaves.",
        "organic"    : "Remove infected plant material. Improve drainage around field.",
        "chemical"   : "Tebuconazole or Propiconazole. Spray at first sign, repeat after 14 days.",
        "prevention" : "Use resistant varieties. Rotate with beans or sunflower. Avoid dense planting.",
        "urgency"    : "Act immediately — can destroy entire crop in severe cases.",
        "local_tip"  : "Peak risk during long rains. Report to your local agriculture extension officer if widespread.",
    },
    "Corn_(maize)___healthy": {
        "disease"    : "Healthy Maize",
        "crop"       : "Maize",
        "severity"   : "none",
        "symptoms"   : "No disease detected. Maize appears healthy.",
        "organic"    : "Apply compost or cattle manure for strong growth.",
        "chemical"   : "No treatment needed.",
        "prevention" : "Rotate crops, use certified seeds, scout weekly.",
        "urgency"    : "None.",
        "local_tip"  : "Healthy maize is critical for food security. Protect it with good cultural practices.",
    },

    # ── GRAPE ────────────────────────────────────────────────────
    "Grape___Black_rot": {
        "disease"    : "Grape Black Rot",
        "crop"       : "Grape",
        "severity"   : "high",
        "symptoms"   : "Tan-brown circular spots on leaves; shrivelled black 'mummies' on fruit.",
        "organic"    : "Remove and destroy all mummified berries and infected leaves immediately.",
        "chemical"   : "Mancozeb or Myclobutanil. Begin at bud break, repeat every 10–14 days.",
        "prevention" : "Train vines for airflow. Remove mummies before season. Avoid wetting leaves.",
        "urgency"    : "Act within 24 hours. Black rot destroys entire clusters quickly.",
        "local_tip"  : "Less common in Kenya but possible in Rift Valley highlands. Consult extension officer.",
    },
    "Grape___Esca_(Black_Measles)": {
        "disease"    : "Grape Esca (Black Measles)",
        "crop"       : "Grape",
        "severity"   : "high",
        "symptoms"   : "Tiger-striped leaves, dark brown wood inside canes, sudden wilting ('apoplexy').",
        "organic"    : "No effective organic cure. Remove and burn infected canes immediately.",
        "chemical"   : "No fully effective chemical treatment. Trichoderma bioagent on pruning wounds.",
        "prevention" : "Seal all pruning cuts with wound paste. Use clean, sterilised pruning tools.",
        "urgency"    : "Long-term management disease. Remove infected vines to protect neighbours.",
        "local_tip"  : "Prevention through pruning hygiene is the only reliable strategy.",
    },
    "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)": {
        "disease"    : "Grape Leaf Blight",
        "crop"       : "Grape",
        "severity"   : "medium",
        "symptoms"   : "Irregular dark brown spots on older leaves, sometimes with yellow halo.",
        "organic"    : "Remove infected leaves. Apply copper-based spray (copper oxychloride 50g/L).",
        "chemical"   : "Chlorothalonil or Mancozeb every 10–14 days.",
        "prevention" : "Ensure good canopy ventilation. Avoid waterlogged soil.",
        "urgency"    : "Treat within 5 days of first spots appearing.",
        "local_tip"  : "Avoid overhead irrigation on grape leaves, water at soil level only.",
    },
    "Grape___healthy": {
        "disease"    : "Healthy Grape",
        "crop"       : "Grape",
        "severity"   : "none",
        "symptoms"   : "No disease detected.",
        "organic"    : "Maintain with regular pruning and compost application.",
        "chemical"   : "No treatment needed.",
        "prevention" : "Regular scouting and good canopy management.",
        "urgency"    : "None.",
        "local_tip"  : "Grapes thrive in dry highland areas of Kenya with irrigation.",
    },

    # ── ORANGE ───────────────────────────────────────────────────
    "Orange___Haunglongbing_(Citrus_greening)": {
        "disease"    : "Citrus Greening (HLB)",
        "crop"       : "Orange / Citrus",
        "severity"   : "high",
        "symptoms"   : "Asymmetric 'blotchy mottle' yellowing on leaves. Bitter, misshapen fruit. Stunted growth.",
        "organic"    : "No cure. Remove and burn infected trees to stop spread. Boost tree health with zinc foliar spray.",
        "chemical"   : "Control the psyllid vector with imidacloprid or thiamethoxam insecticides.",
        "prevention" : "Plant certified disease-free nursery stock only. Control Asian citrus psyllid.",
        "urgency"    : "CRITICAL — report to Kenya Plant Health Inspectorate (KEPHIS) immediately.",
        "local_tip"  : "HLB is a serious regulated disease in Kenya. Contact KEPHIS: 0800 720 757.",
    },

    # ── PEACH ────────────────────────────────────────────────────
    "Peach___Bacterial_spot": {
        "disease"    : "Peach Bacterial Spot",
        "crop"       : "Peach",
        "severity"   : "medium",
        "symptoms"   : "Small, water-soaked spots on leaves that turn brown; sunken spots on fruit.",
        "organic"    : "Copper hydroxide spray (copper-based bactericide). Apply at petal fall.",
        "chemical"   : "Copper oxychloride + Mancozeb combination spray. Repeat every 10 days.",
        "prevention" : "Plant resistant peach varieties. Avoid working in the orchard when wet.",
        "urgency"    : "Treat within 5 days of first symptoms.",
        "local_tip"  : "Most severe after rain. Scout after every rainstorm.",
    },
    "Peach___healthy": {
        "disease"    : "Healthy Peach",
        "crop"       : "Peach",
        "severity"   : "none",
        "symptoms"   : "No disease detected.",
        "organic"    : "Apply well-rotted compost around base annually.",
        "chemical"   : "No treatment needed.",
        "prevention" : "Annual pruning and regular inspection.",
        "urgency"    : "None.",
        "local_tip"  : "Peaches grow well in Kenyan highlands (1,500–2,200m elevation).",
    },

    # ── PEPPER ───────────────────────────────────────────────────
    "Pepper,_bell___Bacterial_spot": {
        "disease"    : "Pepper Bacterial Spot",
        "crop"       : "Bell Pepper",
        "severity"   : "medium",
        "symptoms"   : "Water-soaked lesions on leaves that dry to brown. Raised scabs on fruit.",
        "organic"    : "Copper oxychloride spray. Remove infected leaves. Avoid overhead watering.",
        "chemical"   : "Copper-based bactericide (Kocide, Cuprofix). Apply every 5–7 days in wet weather.",
        "prevention" : "Use certified disease-free seed. Crop rotation (avoid peppers/tomatoes in same spot).",
        "urgency"    : "Treat within 3 days — spreads rapidly through water splash.",
        "local_tip"  : "Very common in Kenyan lowland vegetable farms. Drip irrigation reduces risk significantly.",
    },
    "Pepper,_bell___healthy": {
        "disease"    : "Healthy Bell Pepper",
        "crop"       : "Bell Pepper",
        "severity"   : "none",
        "symptoms"   : "No disease detected.",
        "organic"    : "Mulch with dry grass to retain moisture and suppress weeds.",
        "chemical"   : "No treatment needed.",
        "prevention" : "Stake plants, ensure drainage, rotate crops each season.",
        "urgency"    : "None.",
        "local_tip"  : "Peppers do well in Kenyan lowlands with drip irrigation.",
    },

    # ── POTATO ───────────────────────────────────────────────────
    "Potato___Early_blight": {
        "disease"    : "Potato Early Blight",
        "crop"       : "Potato",
        "severity"   : "medium",
        "symptoms"   : "Dark brown concentric ring 'target' spots on older leaves. Premature defoliation.",
        "organic"    : "Neem cake soil application. Spray 1% neem oil solution every 7 days.",
        "chemical"   : "Mancozeb (Dithane M45) or Chlorothalonil. Spray every 7–10 days.",
        "prevention" : "Use certified seed potatoes. Remove infected foliage. Crop rotation.",
        "urgency"    : "Treat within 5 days. Can reduce yield by 30% if ignored.",
        "local_tip"  : "Very common in Kinangop, Meru, and Nyandarua potato belts of Kenya.",
    },
    "Potato___Late_blight": {
        "disease"    : "Potato Late Blight",
        "crop"       : "Potato",
        "severity"   : "high",
        "symptoms"   : "Pale green to brown water-soaked patches on leaves; white fuzzy mould underneath. Foul smell.",
        "organic"    : "Remove and burn infected plants immediately. Apply copper oxychloride solution.",
        "chemical"   : "Metalaxyl+Mancozeb (Ridomil Gold MZ) is most effective. Spray every 5–7 days.",
        "prevention" : "Plant certified blight-resistant varieties (e.g., Dutch Robyjn). Avoid dense canopy.",
        "urgency"    : "URGENT — Late blight destroys fields in 7–10 days. Act immediately.",
        "local_tip"  : "Caused by P. infestans — the same disease as the Irish Famine. Report large outbreaks to extension officers.",
    },
    "Potato___healthy": {
        "disease"    : "Healthy Potato",
        "crop"       : "Potato",
        "severity"   : "none",
        "symptoms"   : "No disease detected.",
        "organic"    : "Maintain earthing-up and apply compost at planting.",
        "chemical"   : "No treatment needed.",
        "prevention" : "Use certified seed, scout weekly, maintain spacing.",
        "urgency"    : "None.",
        "local_tip"  : "Good hilling (mounding soil around base) improves yield and reduces disease.",
    },

    # ── RASPBERRY ────────────────────────────────────────────────
    "Raspberry___healthy": {
        "disease"    : "Healthy Raspberry",
        "crop"       : "Raspberry",
        "severity"   : "none",
        "symptoms"   : "No disease detected.",
        "organic"    : "Apply mulch around canes. Remove old canes after fruiting.",
        "chemical"   : "No treatment needed.",
        "prevention" : "Annual cane pruning and tying to supports.",
        "urgency"    : "None.",
        "local_tip"  : "Raspberries thrive in Kenyan highlands at 1,800–2,500m.",
    },

    # ── SOYBEAN ──────────────────────────────────────────────────
    "Soybean___healthy": {
        "disease"    : "Healthy Soybean",
        "crop"       : "Soybean",
        "severity"   : "none",
        "symptoms"   : "No disease detected.",
        "organic"    : "Inoculate seeds with Bradyrhizobium japonicum before planting for nitrogen fixation.",
        "chemical"   : "No treatment needed.",
        "prevention" : "Crop rotation with maize. Avoid waterlogged soils.",
        "urgency"    : "None.",
        "local_tip"  : "Soybean is a valuable cash crop in western Kenya. Consult Western Seed Company for varieties.",
    },

    # ── SQUASH ───────────────────────────────────────────────────
    "Squash___Powdery_mildew": {
        "disease"    : "Squash Powdery Mildew",
        "crop"       : "Squash / Pumpkin",
        "severity"   : "medium",
        "symptoms"   : "White powdery patches on upper leaf surface. Leaves turn yellow and dry out.",
        "organic"    : "Mix 1 tbsp baking soda + 1 tsp vegetable oil + 1 tsp soap in 1L water. Spray every 5 days.",
        "chemical"   : "Sulfur fungicide or Triadimefon. Spray in the morning, avoid midday heat.",
        "prevention" : "Space plants widely. Avoid excess nitrogen. Water at base of plant.",
        "urgency"    : "Treat within 5 days. Spreads in dry, warm conditions.",
        "local_tip"  : "Powdery mildew thrives in dry weather with cool nights — common in Kenya's short rains.",
    },

    # ── STRAWBERRY ───────────────────────────────────────────────
    "Strawberry___Leaf_scorch": {
        "disease"    : "Strawberry Leaf Scorch",
        "crop"       : "Strawberry",
        "severity"   : "medium",
        "symptoms"   : "Dark purple to red spots on upper leaf surface; leaves appear scorched at margins.",
        "organic"    : "Remove infected leaves. Apply neem oil spray. Avoid overhead watering.",
        "chemical"   : "Captan or Copper hydroxide fungicide every 10–14 days.",
        "prevention" : "Plant certified runners only. Good spacing for airflow. Remove old foliage after harvest.",
        "urgency"    : "Treat within 5–7 days to prevent leaf loss.",
        "local_tip"  : "Strawberries are a growing cash crop in Murang'a and Kiambu. Scout weekly.",
    },
    "Strawberry___healthy": {
        "disease"    : "Healthy Strawberry",
        "crop"       : "Strawberry",
        "severity"   : "none",
        "symptoms"   : "No disease detected.",
        "organic"    : "Apply organic mulch. Remove runners to concentrate energy in fruit.",
        "chemical"   : "No treatment needed.",
        "prevention" : "Regular scouting. Use certified runners from reputable nurseries.",
        "urgency"    : "None.",
        "local_tip"  : "Strawberries do well in Kenyan highlands with drip irrigation for high-value income.",
    },

    # ── TOMATO ───────────────────────────────────────────────────
    "Tomato___Bacterial_spot": {
        "disease"    : "Tomato Bacterial Spot",
        "crop"       : "Tomato",
        "severity"   : "medium",
        "symptoms"   : "Small, dark water-soaked spots on leaves, stems, and fruit. Fruit has raised scabs.",
        "organic"    : "Copper oxychloride spray. Remove infected leaves. Avoid wetting foliage.",
        "chemical"   : "Copper-based bactericide (Kocide 3000 or Cuprofix). Apply every 7 days.",
        "prevention" : "Drip irrigate. Use resistant varieties. Rotate crops. Disinfect tools.",
        "urgency"    : "Treat within 3 days — spreads through rain splash and wind.",
        "local_tip"  : "Most common in rainy season in Naivasha, Thika, and Meru tomato farms.",
    },
    "Tomato___Early_blight": {
        "disease"    : "Tomato Early Blight",
        "crop"       : "Tomato",
        "severity"   : "medium",
        "symptoms"   : "Brown target-ring lesions on older lower leaves. Premature defoliation.",
        "organic"    : "Remove infected leaves immediately. Spray neem oil (2%) weekly.",
        "chemical"   : "Mancozeb or Chlorothalonil every 7–10 days. Apply in the morning.",
        "prevention" : "Use certified seed, stake plants for airflow, mulch to prevent soil splash.",
        "urgency"    : "Treat within 5 days to prevent defoliation and yield loss.",
        "local_tip"  : "Very common in Kenyan tomato farms. Stake all plants to reduce leaf-soil contact.",
    },
    "Tomato___Late_blight": {
        "disease"    : "Tomato Late Blight",
        "crop"       : "Tomato",
        "severity"   : "high",
        "symptoms"   : "Large dark green/brown water-soaked patches. White fuzzy mould on underside. Fruit turns brown and rots.",
        "organic"    : "Remove and burn infected plants. Do NOT compost. Apply copper oxychloride.",
        "chemical"   : "Metalaxyl + Mancozeb (Ridomil Gold MZ). Spray every 5–7 days in wet conditions.",
        "prevention" : "Avoid overhead irrigation. Use disease-resistant varieties. Scout daily during rains.",
        "urgency"    : "CRITICAL — can destroy a field in under 2 weeks. Act within 24 hours.",
        "local_tip"  : "Major cause of tomato crop failure in Kenya's rainy season. Report outbreaks to extension officers.",
    },
    "Tomato___Leaf_Mold": {
        "disease"    : "Tomato Leaf Mold",
        "crop"       : "Tomato",
        "severity"   : "medium",
        "symptoms"   : "Yellow patches on upper leaf surface. Olive-green to grey mould on underside.",
        "organic"    : "Improve ventilation in greenhouse. Remove infected leaves. Neem oil spray.",
        "chemical"   : "Mancozeb or Copper hydroxide. Apply preventively in humid conditions.",
        "prevention" : "Increase spacing. Open greenhouse vents. Avoid high humidity (keep below 85%).",
        "urgency"    : "Treat within 5–7 days. Common in greenhouses.",
        "local_tip"  : "Very common in Kenyan greenhouse tomato production. Open vents at midday.",
    },
    "Tomato___Septoria_leaf_spot": {
        "disease"    : "Tomato Septoria Leaf Spot",
        "crop"       : "Tomato",
        "severity"   : "medium",
        "symptoms"   : "Circular spots with grey centres and dark borders on lower leaves. Tiny black dots inside spots.",
        "organic"    : "Remove infected leaves. Apply copper spray. Mulch to reduce soil splash.",
        "chemical"   : "Chlorothalonil or Mancozeb every 7–10 days from first symptom.",
        "prevention" : "Crop rotation (3-year cycle). Stake plants. Drip irrigate.",
        "urgency"    : "Treat within 5 days to prevent complete defoliation.",
        "local_tip"  : "Spreads through rain — common in Kenya's long rains season (March–May).",
    },
    "Tomato___Spider_mites Two-spotted_spider_mite": {
        "disease"    : "Tomato Spider Mites",
        "crop"       : "Tomato",
        "severity"   : "medium",
        "symptoms"   : "Fine webbing on leaves. Tiny yellow/bronze stippling on upper surface. Leaf curling.",
        "organic"    : "Spray strong water jet to dislodge mites. Apply neem oil or garlic spray. Introduce predatory mites.",
        "chemical"   : "Abamectin (Dynamec) or Bifenazate miticide. Rotate chemicals to prevent resistance.",
        "prevention" : "Monitor regularly, especially in dry conditions. Avoid excessive nitrogen.",
        "urgency"    : "Treat within 3–5 days. Populations explode quickly in dry, hot weather.",
        "local_tip"  : "Worst during dry spells in Kenya. Irrigate to maintain humidity and reduce mite pressure.",
    },
    "Tomato___Target_Spot": {
        "disease"    : "Tomato Target Spot",
        "crop"       : "Tomato",
        "severity"   : "medium",
        "symptoms"   : "Brown circular lesions with concentric rings (target appearance) on leaves and fruit.",
        "organic"    : "Remove infected leaves. Improve airflow. Apply neem oil spray.",
        "chemical"   : "Tebuconazole or Azoxystrobin fungicide. Spray every 10 days.",
        "prevention" : "Stake plants. Crop rotation. Avoid excessive leaf wetness.",
        "urgency"    : "Treat within 5 days.",
        "local_tip"  : "Common in humid lowland Kenya. Greenhouse growers in Naivasha report this frequently.",
    },
    "Tomato___Tomato_Yellow_Leaf_Curl_Virus": {
        "disease"    : "Tomato Yellow Leaf Curl Virus (TYLCV)",
        "crop"       : "Tomato",
        "severity"   : "high",
        "symptoms"   : "Upward curling and yellowing of leaves. Stunted plant. Very few or no fruit set.",
        "organic"    : "Remove and burn infected plants. No chemical cure for the virus itself.",
        "chemical"   : "Control whitefly vector with Imidacloprid or Thiamethoxam. Use yellow sticky traps.",
        "prevention" : "Plant TYLCV-resistant varieties (e.g., Tylka F1, Kilele F1 — available in Kenya). Use insect netting.",
        "urgency"    : "Remove infected plants immediately to prevent whitefly spread to neighbours.",
        "local_tip"  : "TYLCV is widespread in lowland Kenya. Buy resistant seeds from certified dealers (BASFKE, East African Seeds).",
    },
    "Tomato___Tomato_mosaic_virus": {
        "disease"    : "Tomato Mosaic Virus (ToMV)",
        "crop"       : "Tomato",
        "severity"   : "high",
        "symptoms"   : "Light and dark green mosaic pattern on leaves. Leaf distortion. Stunted growth.",
        "organic"    : "Remove infected plants. Wash hands before handling plants. No cure.",
        "chemical"   : "No effective chemical treatment. Control aphid vectors with insecticidal soap.",
        "prevention" : "Use certified virus-free seed. Disinfect tools with 10% bleach solution. No smoking near plants.",
        "urgency"    : "Remove infected plants within 24 hours to reduce spread.",
        "local_tip"  : "Spreads through contact, tools, and aphids. Train farm workers on hygiene practices.",
    },
    "Tomato___healthy": {
        "disease"    : "Healthy Tomato",
        "crop"       : "Tomato",
        "severity"   : "none",
        "symptoms"   : "No disease detected. Plant appears healthy.",
        "organic"    : "Continue with compost tea foliar feeds for strong immunity.",
        "chemical"   : "No treatment needed.",
        "prevention" : "Scout weekly. Use preventive copper spray during rainy seasons.",
        "urgency"    : "None.",
        "local_tip"  : "Tomato is Kenya's most important vegetable. Protect your investment with weekly scouting.",
    },
}


def get_treatment(class_name: str) -> dict:
    """
    Look up treatment for a predicted disease class.
    Returns a safe default if the class is not in the database.
    """
    info = TREATMENTS.get(class_name)
    if info is None:
        # Graceful fallback for unknown classes (e.g., custom-added crops)
        crop = class_name.replace("___", " - ").replace("_", " ")
        return {
            "disease"    : crop,
            "crop"       : "Unknown",
            "severity"   : "unknown",
            "symptoms"   : "No detailed information available for this class.",
            "organic"    : "Consult your local agriculture extension officer.",
            "chemical"   : "Contact your nearest agrovet for advice.",
            "prevention" : "Practice good crop hygiene and regular scouting.",
            "urgency"    : "Consult an expert promptly.",
            "local_tip"  : "Call the Kenya Farmers Helpline: 0800 723 022 (Toll-free).",
        }
    return info


def list_all_diseases() -> list:
    """Return sorted list of all disease class keys."""
    return sorted(TREATMENTS.keys())
