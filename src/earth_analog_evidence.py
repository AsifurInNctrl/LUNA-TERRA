"""Literature-grounded Earth analog research candidates; not quantitative results."""

from __future__ import annotations


STATUS = "Literature-supported research candidate — not yet quantitatively assessed by LUNA-TERRA."

DIMENSIONS = {
    "geology": "Geological structure and landforms",
    "geochemistry": "Mineralogy and geochemistry",
    "water_ice": "Water, ice and volatile processes",
    "extremes": "Thermal and environmental extremes",
    "terrain": "Terrain and surface morphology",
    "operations": "Exploration operations and logistical constraints",
    "astrobiology": "Astrobiology and biosignature preservation",
}


EARTH_ANALOGS = [
    {
        "id": "atacama",
        "name": "Atacama Desert, Chile",
        "purpose": "Investigate selected aspects of Martian hyperaridity, soil geochemistry, and the preservation and detection of biosignatures.",
        "planetary_target": "Mars — hyperarid soils, salts, environmental gradients, and life-detection context.",
        "dimensions": ["geochemistry", "water_ice", "extremes", "astrobiology"],
        "evidence": (
            "Boy et al. (2022) measured soil water, salts, organic carbon and related properties along distinct Atacama gradients. "
            "Their results show that aridity interacts with geography, altitude, and local ecosystems; a north–south transect isolated an aridity gradient more clearly than the more complex west–east transects. "
            "NASA Astrobiology describes selected Atacama sites as settings for testing Mars life-detection instruments and drilling operations."
        ),
        "interpretation": "Use defined transects and sampled soils to study particular hyperarid and geochemical processes; do not treat the entire desert as one environment or as a Mars replica.",
        "limitations": [
            "Conditions vary across the desert, including strong spatial and elevation gradients.",
            "Nearby productive ecosystems and local effects can shape observed biology and soil properties.",
            "Aridity alone does not capture mineralogy, radiation, atmospheric pressure, or the full environmental history of Mars.",
        ],
        "data_needed": "Georeferenced field samples with depth, soil-water content, soluble-ion/mineralogy, organic-carbon or biosignature protocols, meteorology and transect metadata; matched orbital spectral and terrain products for the exact sampled footprints.",
        "sources": [
            {"label": "Boy et al. (2022), Journal of Geophysical Research: Biogeosciences", "url": "https://doi.org/10.1029/2021JG006714", "kind": "Peer-reviewed primary research"},
            {"label": "NASA Astrobiology — Atacama Desert field site", "url": "https://astrobiology.nasa.gov/research-locations/", "kind": "NASA research-location summary"},
        ],
    },
    {
        "id": "haughton",
        "name": "Haughton Impact Crater, Devon Island, Canada",
        "purpose": "Investigate impact geology, cold-desert and ground-ice processes, field exploration methods, and operational isolation.",
        "planetary_target": "Moon and Mars — impact structures and exploration operations; Mars — selected cold-desert and permafrost questions.",
        "dimensions": ["geology", "water_ice", "extremes", "terrain", "operations"],
        "evidence": (
            "The NASA Haughton-Mars Project expedition report documents field research and logistics at the remote Arctic impact-crater site. "
            "NASA's analog-missions overview describes Haughton as a rocky, dry, ancient-crater setting used to test exploration technologies and operations. "
            "These sources support a process and operations analogy; the cited records do not make Haughton a quantitative match for a lunar or Martian site."
        ),
        "interpretation": "A bounded field setting for examining impact structure, polar-desert field work, and operational constraints. Claims about ground ice should be tied to a specific Haughton field area and direct geocryological evidence.",
        "limitations": [
            "Earth's gravity and atmosphere differ from the Moon and Mars.",
            "Terrestrial hydrology, weathering, and biological processes alter the surface and subsurface.",
            "The crater and polar setting do not establish equivalence to a specific planetary crater or landing site.",
        ],
        "data_needed": "Authoritative crater and field-area boundaries; consistent-resolution DEM and imagery; mapped impact lithologies and structures; georeferenced permafrost/ground-ice observations; seasonal weather and field-operation logs.",
        "sources": [
            {"label": "de Weck & Simchi-Levi (2006), NASA/TP—2006–214196, Haughton-Mars Project Expedition 2005 Final Report", "url": "https://ntrs.nasa.gov/api/citations/20060013129/downloads/20060013129.pdf", "kind": "NASA technical report"},
            {"label": "NASA (2011), NASA’s Analog Missions: Paving the Way for Space Exploration", "url": "https://www.nasa.gov/wp-content/uploads/2015/06/563511main_nasa-analog-missions-06-2011_508.pdf", "kind": "NASA program overview"},
        ],
    },
    {
        "id": "mcmurdo",
        "name": "McMurdo Dry Valleys, Antarctica",
        "purpose": "Investigate selected Martian cold-desert geomorphology, dry permafrost, subsurface ice, and constraints on field exploration.",
        "planetary_target": "Mars — cold-desert surface and near-surface processes, especially permafrost and ground ice.",
        "dimensions": ["geology", "water_ice", "extremes", "terrain", "operations", "astrobiology"],
        "evidence": (
            "The 2013 Planetary and Space Science study compares upper Dry Valleys geomorphology and ground ice with Mars observations and reports distinct cryostratigraphy even between nearby valleys. "
            "NASA Astrobiology separately describes University Valley as an ice-cemented-ground and subsurface sampling analogue, and the wider Dry Valleys as a setting for life-detection work."
        ),
        "interpretation": "The Dry Valleys are a geographically varied Mars surface/permafrost research region. Comparisons must specify valley, elevation, landform, and process rather than generalize a single site to all of Antarctica.",
        "limitations": [
            "Earth retains an atmosphere, seasonal solar forcing, liquid-water episodes, and active ecosystems.",
            "Dry Valley conditions vary by valley, elevation, aspect, and microclimate.",
            "Similar surface forms do not prove identical formation mechanisms; ground-ice type needs direct measurements.",
        ],
        "data_needed": "A named valley/AOI; matched-resolution terrain and imagery; permafrost temperature and cryostratigraphy; ground-ice type/depth observations; meteorological and seasonal hydrology records; explicit field-to-orbital spatial links.",
        "supporting_extension": {
            "name": "West Lake Bonney (separate sub-ice research extension)",
            "purpose": "Study an ice-covered lake, its aqueous chemistry and sub-ice ecology as a potential process analogue for sub-ice habitats on icy worlds.",
            "evidence": "NASA describes West Lake Bonney as a perennially ice-covered lake used for aqueous chemistry, bathymetry, and under-ice interface mapping.",
            "limitation": "Lake Bonney is a lake-specific sub-ice ecosystem case. It is not interchangeable with the Dry Valleys' cold-desert surface and permafrost analogue, and it is not a direct lunar or Mars landing-site analogue.",
            "source": {"label": "NASA Astrobiology — West Lake Bonney field site", "url": "https://astrobiology.nasa.gov/research-locations/", "kind": "NASA research-location summary"},
        },
        "sources": [
            {"label": "Heldmann et al. (2013), The high elevation Dry Valleys in Antarctica as analog sites for subsurface ice on Mars", "url": "https://doi.org/10.1016/j.pss.2013.05.019", "kind": "Peer-reviewed primary research"},
            {"label": "Salvatore & Levy (2021), The McMurdo Dry Valleys of Antarctica: a geological, environmental, and ecological analog to the Martian surface and near surface", "url": "https://doi.org/10.1016/B978-0-12-820245-6.00011-2", "kind": "Peer-reviewed synthesis chapter"},
            {"label": "NASA Astrobiology — McMurdo Dry Valleys and University Valley field sites", "url": "https://astrobiology.nasa.gov/research-locations/", "kind": "NASA research-location summary"},
        ],
    },
    {
        "id": "lonar",
        "name": "Lonar Impact Crater, Maharashtra, India",
        "purpose": "Investigate impact cratering in basaltic target rocks, impact breccias, alteration, and crater degradation for specific lunar and Martian geology questions.",
        "planetary_target": "Moon and Mars — impact processes; Mars — basaltic target materials and post-impact alteration.",
        "dimensions": ["geology", "geochemistry", "water_ice", "terrain"],
        "evidence": (
            "USGS-indexed studies describe Lonar as an impact crater in Deccan basalt. Fredriksson et al. report shock-metamorphosed materials, breccias, and glass spherules; Hagerty and Newsom describe basaltic impact breccias and post-impact hydrothermal alteration. "
            "The evidence supports comparison of selected impact and basalt-alteration processes, not a direct match in crater evolution."
        ),
        "interpretation": "Useful for impact products and basaltic target-rock comparisons; distinguish impact evidence from the modern lake and its terrestrial hydrological setting.",
        "limitations": [
            "Earth gravity differs from lunar and Martian gravity and affects crater scaling and morphology.",
            "Monsoon hydrology, erosion, weathering, and human land use modify the crater.",
            "Present-day lake chemistry is not evidence of lunar or Martian volatile conditions.",
        ],
        "data_needed": "Mapped crater rim/floor/ejecta AOIs; DEM and imagery at controlled resolution; lithology, shock, breccia and alteration-mineral maps/samples; dated stratigraphic context; erosion and hydrology observations for separating impact from later modification.",
        "sources": [
            {"label": "Fredriksson et al. (1973), Lonar Lake, India: An impact crater in basalt", "url": "https://doi.org/10.1126/science.180.4088.862", "kind": "Peer-reviewed primary research (USGS record)"},
            {"label": "Hagerty & Newsom (2003), Hydrothermal alteration at the Lonar Lake impact structure, India", "url": "https://pubs.usgs.gov/publication/70202247", "kind": "Peer-reviewed primary research (USGS record)"},
            {"label": "USGS publication record 70010158", "url": "https://pubs.usgs.gov/publication/70010158", "kind": "USGS bibliographic record"},
        ],
    },
    {
        "id": "rio_tinto",
        "name": "Río Tinto, Spain",
        "purpose": "Investigate acidic aqueous geochemistry, iron- and sulfur-bearing mineral formation/alteration, and biosignature detection in a selected Mars-relevant context.",
        "planetary_target": "Mars — selected ancient acidic-water, iron/sulfur mineralogy, and astrobiology questions.",
        "dimensions": ["geochemistry", "water_ice", "astrobiology"],
        "evidence": (
            "Amils et al. (2014) review Río Tinto as a geochemical and mineralogical Mars analogue, describing acidic, iron-rich waters, mineral assemblages, and microbial systems. "
            "NASA Astrobiology lists the site among research locations. These sources support specialized geochemical and astrobiology questions, not modern Mars surface equivalence."
        ),
        "interpretation": "Treat Río Tinto as a process end-member for acidic water-rock alteration and associated mineral/biosignature detection; do not extend the analogy to lunar terrain or site suitability.",
        "limitations": [
            "The modern river is a terrestrial aqueous environment and is not a direct analogue for current Mars surface conditions.",
            "The analogy concerns selected geochemical and mineralogical processes; Earth and Mars histories and boundary conditions differ.",
            "It has no stated relevance here to lunar terrain or landing-site suitability.",
        ],
        "data_needed": "Georeferenced water chemistry (pH, redox, dissolved ions), mineral/stratigraphic maps and spectra, seasonal discharge context, microbial/biosignature sampling metadata, and matched Mars orbital/rover mineralogy products with comparable detection limits.",
        "sources": [
            {"label": "Amils et al. (2014), Río Tinto: A Geochemical and Mineralogical Terrestrial Analogue of Mars", "url": "https://doi.org/10.3390/life4030511", "kind": "Peer-reviewed review"},
            {"label": "Amils et al. (2005), The Rio Tinto basin, Spain: Mineralogy, sedimentary geobiology, and implications for interpretation of outcrop rocks at Meridiani Planum, Mars", "url": "https://doi.org/10.1016/j.epsl.2005.09.043", "kind": "Peer-reviewed research"},
            {"label": "NASA Astrobiology — research locations", "url": "https://astrobiology.nasa.gov/research-locations/", "kind": "NASA research-location directory"},
        ],
    },
]


def validate_evidence_records(records: list[dict] = EARTH_ANALOGS) -> None:
    """Raise ValueError when candidate records miss required evidence boundaries."""
    ids: set[str] = set()
    for record in records:
        if not record.get("id") or record["id"] in ids:
            raise ValueError("Each Earth analog record must have a unique non-empty id")
        ids.add(record["id"])
        if not record.get("purpose", "").strip():
            raise ValueError(f"{record.get('name', record['id'])} has no named research purpose")
        sources = record.get("sources", [])
        if not sources or not any(source.get("url", "").startswith(("https://", "http://")) for source in sources):
            raise ValueError(f"{record.get('name', record['id'])} needs a verifiable source URL")
        if not record.get("limitations") or not all(item.strip() for item in record["limitations"]):
            raise ValueError(f"{record.get('name', record['id'])} must state specific limitations")
        if record.get("status") not in (None, STATUS):
            raise ValueError(f"{record['name']} has an inconsistent evidence status")
        if any(term in record for term in ("score", "similarity_score", "rank", "ranking")):
            raise ValueError(f"{record['name']} must not define a score or ranking")
    dry_valleys = next((record for record in records if record["id"] == "mcmurdo"), None)
    if not dry_valleys or not dry_valleys.get("supporting_extension", {}).get("name", "").startswith("West Lake Bonney"):
        raise ValueError("McMurdo Dry Valleys and West Lake Bonney must remain distinguishable")


validate_evidence_records()
