# LUNA-TERRA — Research Basis and Data Feasibility Matrix

| Field | Value |
|---|---|
| **Project** | LUNA-TERRA — Planetary Analog Discovery Platform |
| **Challenge** | NASA Space Apps Challenge 2026 — “Identify Earth Locations that Analog the Permanent Moon Base Locations and Mars” |
| **Prepared** | 14 November 2026 |

**Status:** Literature-led preliminary research and proposed roadmap; datasets have not yet been queried for exact-area coverage or downloaded. No AOIs are finalized, no analysis has been implemented, and no LUNA-TERRA result has been produced.

---

## 1. Research approach and scope

LUNA-TERRA will identify **purpose-specific Earth analog environments** for selected lunar and Martian reference regions. It will not claim that one Earth location reproduces an entire planetary environment.

The approach is:

1. Use peer-reviewed planetary-science research and NASA mission studies to choose reference regions and scientifically relevant variables.
2. Audit the actual Earth, Moon, and Mars datasets available for those variables.
3. Reproduce a small number of published analog comparisons as benchmarks.
4. Use those benchmarks to screen for additional, less-characterized Earth candidates.
5. Report similarities, differences, data limitations, and uncertainty separately.

The NASA challenge explicitly calls for using open Earth, Moon, and Mars data to identify and characterize **new terrestrial analogs**. It names places such as Atacama, Haughton Crater, and Death Valley as examples, and cautions that existing analog sites are not entirely well characterized.

**Important distinction:** The sources below support the scientific criteria and benchmark environments. They do not, by themselves, prove that any new Earth site is an analog. New candidates require measurements and validation.

### Evidence and decision labels

- **Published findings:** results and literature summaries explicitly attributed to cited studies or product documentation. Model-derived values remain estimates, not direct measurements or confirmed resources.
- **Proposed LUNA-TERRA decisions:** the provisional reference regions, benchmark pool, candidate products, comparison dimensions, and MVP workflow below. These are design choices informed by literature, not project findings.
- **Unverified hypotheses/work:** whether a proposed Earth site is useful for a selected purpose; whether a proposed product covers an exact AOI at suitable quality; and whether measurements can be compared across bodies. These require data audit, implementation, and validation.

The proposed workflow is a roadmap. The current application does not implement STAC discovery, raster processing, terrain analysis, or similarity scoring.

## 2. Core literature review

### Paper A — Lunar south-pole landing-site science (2026)

| Reference detail | Value |
|---|---|
| Citation | **Wueller et al. (2026), “Assessing Potential Landing Sites With Favorable Illumination and Accessible, Potentially Volatile-Rich Permanently Shadowed Regions Within Artemis Candidate Landing Regions,” Journal of Geophysical Research: Planets, 131, e2025JE009434.** |
| DOI | <https://doi.org/10.1029/2025JE009434> |
| Full text | <https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2025JE009434> |

**What the paper did (source-derived):**

- Identified and evaluated candidate landing sites within Artemis candidate landing regions.
- Used LRO Wide Angle Camera imagery at about **100 m/pixel**, LROC south-polar Narrow Angle Camera mosaics at about **1 m/pixel**, LOLA digital elevation models at **20 m/pixel**, LOLA altimetry tracks, and Diviner south-polar temperature maps at **240 m/pixel**.
- Used the 20 m/pixel LOLA DEM to derive slope maps and identify permanently shadowed regions (PSRs).
- Applied an Artemis Human Landing System slope threshold of **0–8°**, with **0–5° as the goal**, and a 100 m buffer from steeper terrain to account for landing accuracy.
- Considered access to PSRs within roughly **2 km** of a candidate landing site.
- Modeled illumination over mission periods. For a 6.5-day surface mission, the study used at least **10 consecutive illuminated days** as a buffered criterion.
- Used Diviner temperatures and modeled PSR crater ages to assess potential volatile preservation. The authors explicitly note important uncertainties, including the depth and form of possible volatiles and limitations of crater-age modeling.

**Primary lunar reference proposed for LUNA-TERRA: PNS02 (Peak Near Shackleton).**

The paper identifies PNS02 at approximately **89.061°S, 128.442°E**. It reports five PSR-hosting craters in the exploration zone, with modeled ages of about 1.45–3.2 Ga; accessible slopes no greater than 10° in the study’s PSR-access assessment; yearly average PSR temperatures of about 62–91 K; and an estimated cumulative volatile abundance of roughly 150,540 kg. One approximately 91 K PSR was reported about 250 m from the landing site. These are **model-based estimates, not confirmed reserves of accessible water ice**.

Why this is a sensible provisional scientific reference: the 2026 study analyzes PNS02 within its broader Artemis candidate-region study and supplies explicit topographic, thermal, illumination, and PSR-access methods. NASA’s October 28, 2024 update lists nine Artemis III candidate regions and names Peak Near Cabeus B, not Peak Near Shackleton. Therefore PNS02 is proposed here from the published PNS-region study; it must not be described as one of the nine regions in NASA’s October 2024 updated list. This choice does not itself establish suitability for a permanent Moon base.

**Secondary lunar comparison: CR05 (Connecting Ridge).** The same paper reports approximately 425,582 kg of modeled cumulative volatile potential for CR05 and describes a varied set of nearby PSR-hosting craters. However, the paper notes that Connecting Ridge appeared in NASA’s 2022 candidate list but was excluded from NASA’s 2024 update. Therefore, CR05 should be a secondary scientific comparison, not our primary current Artemis-region case.

**Data availability:** The paper’s landing-site, illumination, crater-age, and PSR/volatile shapefiles are available through Zenodo: <https://doi.org/10.5281/zenodo.17084058>. The article also links LOLA RDR data at <https://imbrium.mit.edu/> and the LROC south-polar NAC mosaic at <https://data.lroc.im-ldi.com/lroc/view_rdr/NAC_POLE_SOUTH>.

### Paper B — De Gerlache–Shackleton ridge characterization (2024)

| Reference detail | Value |
|---|---|
| Citation | **Sathyan et al. (2024), “Potential landing sites characterization on lunar south pole: De-Gerlache to Shackleton ridge region,” Icarus, article 115988.** |
| DOI | <https://doi.org/10.1016/j.icarus.2024.115988> |
| Article page | <https://www.sciencedirect.com/science/article/pii/S0019103524000460> |

**What is supported by the accessible abstract and article record:**

- The paper characterized four sites along the ridge connecting de Gerlache and Shackleton.
- It assessed slope, illumination, surface roughness, surface temperature, access to nearby PSRs, compositional diversity, and rover trafficability.
- It reports C1 at approximately **89.406°S, 136.2°W** and D at approximately **89.003°S, 87.514°W** as the most promising of the four sites in that study, balancing scientific value and exploration feasibility.
- Its dataset/method summary says it integrated high-level data products from Chandrayaan-1, Chandrayaan-2, and LRO, alongside geomorphological and polar-terrain maps, using a GIS workflow.

**Use for LUNA-TERRA:** This paper is a useful independent benchmark for how to combine landing safety, rover mobility, illumination, thermal context, and volatile access. The publisher page was not fully accessible during this review, so we will not infer unverified Table 1 product identifiers, numerical rankings, or processing details from it. Obtain the paper or its supplementary material before attempting a faithful reproduction.

### Paper C — Mars analog environments and multi-scale characterization (2022)

| Reference detail | Value |
|---|---|
| Citation | **Harris et al. (2022), “Remote and in-Situ Characterization of Mars Analogs: Coupling Scales to Improve the Search for Microbial Signatures on Mars,” Frontiers in Astronomy and Space Sciences, 9:849078.** |
| DOI | <https://doi.org/10.3389/fspas.2022.849078> |
| Full text | <https://www.frontiersin.org/journals/astronomy-and-space-sciences/articles/10.3389/fspas.2022.849078/full> |

**What the review says (source-derived):**

The authors review five Earth analog sites against ancient lake systems in Gale and Jezero craters. They emphasize that no terrestrial site is a perfect representation of Martian lakes; the sites are useful for different climatic, geological, geochemical, and biological questions. Their recommended criteria include:

- Geological setting and lithology, especially basaltic, mafic, or ultramafic terrains where relevant.
- Mineralogy, including magnesium carbonates, Fe/Mg clays, amorphous silica, hematite, and sulfates where these are relevant to the Mars target.
- Climate and aridity, including temperature, precipitation, and snow fraction.
- Hydrologic history, water sources, wetting/drying, and lake desiccation.
- Water chemistry, including salinity, pH, and redox potential.
- Multi-scale observations: orbital remote sensing, aerial/drone observations, rover-scale instruments, and in-situ measurements.

**Five benchmark analog sites summarized by the review:**

| Earth analog | Coordinates in the paper | Why the authors include it | Important caveat |
|---|---:|---|---|
| Atacama salars, Chile | 23.60°S, 68.24°W | Hyperarid salt flats, high solar irradiance, evaporitic basins, hypersaline brines, and Mars-relevant salts. | Not a cold polar site; modern brines and surface conditions are not equivalent to ancient Mars. |
| Haughton Impact Crater, Devon Island, Canada | 75.38°N, 89.67°W | Cold, arid polar impact structure with paleolake sediments, impact-shocked rocks, and subsurface biological analog work. | Its lithology and hydrology differ from Jezero; it is a purpose-specific impact/polar analog. |
| Lake Bonney, McMurdo Dry Valleys, Antarctica | 77.71°S, 162.37°E | Polar desert, perennially ice-covered lake, highly stratified saline water, microbial mats, and limited biological confounders. | The review’s listed host geology is not mafic/ultramafic; it is not a direct basaltic analog. |
| Lonar Crater, India | 19.98°N, 76.51°E | Young impact crater in Deccan basalt, with plagioclase and pyroxene; morphologic and basaltic comparison. | Tropical monsoon hydrology, agriculture, and human population create confounding influences. |
| Rio Tinto, Spain | 37.28°N, 6.87°W | Iron- and sulfur-rich acidic aqueous geochemistry; useful as a warm/wet acidic end-member. | Not a cold or hyperarid whole-environment analog. |

The review’s comparison table reports approximate published site-level climate values (compiled from cited literature): Lake Bonney MAAT −17.1 °C and MAP <100 mm; Haughton MAAT −16.4 °C and MAP <13 mm; Atacama salars MAAT 1–14 °C and MAP 50–150 mm; Lonar MAAT 26 °C and MAP 752 mm; Rio Tinto MAAT 16.1 °C and MAP 849.1 mm. These figures are literature summaries, not measurements newly extracted by LUNA-TERRA.

**Use for LUNA-TERRA:** Jezero Crater is our primary Martian reference because the review specifically compares it with analog environments and describes its ancient lake, surface-runoff history, and basaltic setting. Gale remains a useful secondary reference. The five terrestrial sites should be treated as benchmark environments with different analog purposes, not as five equivalent matches.

---

## 3. Provisional reference regions and Earth benchmark pool

| Body / role | Provisional region | Basis | Intended use in LUNA-TERRA | Status |
|---|---|---|---|---|
| Moon — primary reference | **PNS02, Peak Near Shackleton** (89.061°S, 128.442°E) | Wueller et al. (2026), which analyzes PNS within its broader candidate-region study; not one of the nine regions in NASA's October 2024 updated Artemis III list. | Terrain morphology, slope, local relief, PSR proximity, thermal-context visualization, and landing/operations constraints. | Provisional primary scientific reference. Verify exact footprint and coordinate conventions; do not label it a current NASA 2024 Artemis III region. |
| Moon — secondary comparison | **CR05, Connecting Ridge** (89.421°S, 149.472°W) | Wueller et al. (2026); Sathyan et al. (2024) study the wider de Gerlache–Shackleton ridge context. | Compare a site with many nearby PSRs and varied crater ages; test robustness of lunar workflow. | Secondary only; Connecting Ridge was excluded from NASA’s 2024 updated candidate-region list. |
| Mars — primary reference | **Jezero Crater** | Harris et al. (2022); Mars 2020 Perseverance exploration; ancient lake/delta setting. | Terrain, crater/basin/fan morphology, broad lithologic/mineral context, and ancient-lake analog questions. | Provisional primary Mars case. Define an exact Jezero AOI polygon before querying imagery. |
| Earth — benchmark | **Atacama salars** | Harris et al. (2022). | Hyperaridity, evaporitic basins, salts, surface reflectance patterns, and field-geochemistry context for Mars. | Strong benchmark for selected Mars questions. |
| Earth — benchmark | **Haughton Impact Crater** | Harris et al. (2022). | Impact-crater morphology, polar/arid field operations, paleolake sediments. | Strong benchmark for impact/polar questions. |
| Earth — benchmark | **Lake Bonney / McMurdo Dry Valleys** | Harris et al. (2022). | Cold polar-desert logistics, ice-covered lake setting, seasonal meltwater and cryoenvironments. | Strong benchmark for cold/polar operations; not a direct lunar vacuum/radiation analog. |
| Earth — benchmark | **Lonar Crater** | Harris et al. (2022). | Basaltic impact crater morphology and basaltic mineralogy. | Useful geological benchmark; monsoon and human influences are confounders. |
| Earth — benchmark | **Rio Tinto** | Harris et al. (2022). | Iron/sulfate/acidic geochemistry and mineral-detection methods. | Specialized geochemical end-member, not a whole-environment match. |

**New analog discovery rule:** The established sites above are benchmark/reference sites. LUNA-TERRA must subsequently screen other under-characterized environments and clearly label any result as a *candidate* until independent geological or field evidence supports it.

---

## 4. Research-to-measurement matrix

| Comparison dimension | What to measure | Moon reference data | Mars reference data | Earth data / evidence | Comparability and priority |
|---|---|---|---|---|---|
| Terrain slope | Slope distribution, fraction below selected slope bands, adjacency to steep hazards. | LRO LOLA LDEM (20 m/pixel in Wueller et al. 2026). | Jezero CTX DTM (~20 m/pixel) or HiRISE DTM (~1 m/pixel) where available; MOLA for regional context. | Copernicus DEM GLO-30 DSM; use the same DEM source and processing across sites. | **High priority.** Derive with consistent algorithms and compare distributions at a common effective scale. Landing thresholds are engineering constraints, not universal analog scores. |
| Local relief / terrain roughness | Windowed relief, terrain ruggedness, elevation variance, roughness at fixed ground distances. | LOLA LDEM; LOLA RDR tracks for selected detailed profiles. | CTX/HiRISE DTM for local relief; MOLA for broad context. | Copernicus DEM GLO-30; consider local high-resolution DTM only if available consistently. | **High priority.** Define window sizes in metres and avoid comparing raw pixel-scale roughness across different native resolutions. |
| Landform morphology | Crater, ridge, rim, basin, fan, channel, ejecta, and shadowed-depression metrics. | LOLA DEM, LROC WAC/NAC mosaics. | CTX/HiRISE imagery and DTMs; Jezero delta/fan/valley mapping. | Landsat/Sentinel imagery, DEM-derived landforms, and published geological maps. | **High priority for interpretation.** Compare morphometric form and process context; do not imply identical geological age or formation history. |
| Surface reflectance / spectral properties | Calibrated band ratios or validated mineral/land-cover classes; record sensor and bandpass. | LRO/LROC and appropriate lunar spectral products; confirm target coverage/product before selection. | CRISM hyperspectral products; CTX/HiRISE for context. | Landsat C2 L2 surface reflectance; Sentinel-2 L2A; ASTER AST_07/AST_07XT only if the separate surface-reflectance product is available and verified. Microsoft Planetary Computer's `aster-l1t` collection is AST_L1T at-sensor radiance, not surface reflectance. | **Medium priority.** Instruments have different bandpasses, calibration, illumination, atmosphere, and viewing geometry. Do not compare raw band values directly across bodies. Prefer validated mineral classes or within-sensor Earth comparisons. |
| Surface thermal context | Day/night or seasonal temperature distributions, thermal inertia proxies only if supported by the product. | Diviner temperature maps (240 m/pixel in Wueller et al. 2026). | THEMIS thermal products; verify exact Jezero footprint, local time, season, and product type. | Landsat C2 L2 surface-temperature product; a separately verified ASTER AST_08 surface kinetic-temperature product. AST_L1T thermal bands are at-sensor radiance, not surface temperature. | **Medium/low cross-body comparability.** Earth atmosphere, moisture, emissivity, solar geometry, and acquisition time differ. Display as context panels, not one direct temperature-equivalence score. |
| Illumination / shadow | Solar visibility, duration, horizon obstruction, terrain shadows, and time window. | LOLA DEM plus solar geometry / SPICE-based illumination modeling; paper provides derived illumination files. | Local solar geometry and topographic shading if needed for rover operations. | DEM-derived horizon and solar exposure; measured local conditions if available. | **Specialized.** Lunar illumination is mission- and date-dependent. Earth day/night, atmosphere, and seasonal geometry make raw duration non-equivalent. Use mainly for site-operation context. |
| Aridity / climate | Mean air temperature, precipitation, snow fraction, humidity, evaporation, and seasonal range. | Not a lunar climate variable in the terrestrial meteorological sense; use thermal/radiative context instead. | Published paleoclimate and geological context; modern Mars climate products are not equivalent to ancient Jezero lake conditions. | Published site measurements, station records, and/or gridded climate products (e.g., TerraClimate/ERA5-Land after coverage audit). | **Medium for Mars analog screening; not a direct planetary equality.** Do not substitute Landsat land-surface temperature for mean annual air temperature. |
| Hydrology / geochemistry | Water source, salinity, pH, redox, evaporites, wetting/drying, lake/groundwater history. | Volatile/PSR proxies; direct water/ice confirmation remains limited and product-specific. | Jezero/Gale ancient lake interpretations, rover observations, and mineralogical evidence. | Peer-reviewed field studies and in-situ site datasets for Atacama, Haughton, Lake Bonney, Lonar, and Rio Tinto. | **High scientific value but often not derivable from satellite imagery alone.** Use field/literature evidence and mark missing variables explicitly. |
| Mineralogy / lithology | Basaltic/mafic units, clays, carbonates, sulfates, silica, oxides, and alteration context. | Lunar spectral/geological maps; LROC and selected spectral products. | CRISM, rover observations, and published Jezero geological maps. | Geological maps, ASTER, Landsat/Sentinel as supporting evidence, and field literature. | **Medium.** Remote-sensing indices are screening evidence, not a substitute for mineralogical ground truth. |
| Radiation, pressure, gravity, atmosphere | Environmental conditions that strongly differ between planetary bodies. | Not reproduced by Earth optical imagery. | Not reproduced by Earth optical imagery. | No equivalent from the selected Earth-observation products. | **Exclude from the similarity score.** State as fundamental analog limitations. |

---

## 5. Preliminary dataset feasibility matrix

This is a **catalog/product feasibility check**, not confirmation that cloud-free scenes or every file have been retrieved for our exact AOIs.

### Earth observations — Microsoft Planetary Computer

| Collection / product | Published/catalog characteristics | Intended use | Preliminary decision |
|---|---|---|---|
| `landsat-c2-l2` — Landsat Collection 2 Level-2 | Global catalog extent from 1982 onward; atmospherically corrected surface reflectance and surface temperature; collection metadata lists multiple GSD values (30, 60, 100, 120 m) and visible/NIR/SWIR/TIR bands. | Primary Earth optical/thermal context for Atacama, Haughton, McMurdo, Lonar, and other candidate AOIs where scenes exist. | **Primary Earth imagery collection.** Query exact AOIs and filter by cloud/QA before download. Respect band-specific resolution; do not treat all outputs as native 30 m. |
| `sentinel-2-l2a` — Sentinel-2 Level-2A | Global catalog extent from 2015 onward; 13 bands at 10, 20, and 60 m; bottom-of-atmosphere reflectance; approximately five-day revisit. | Detailed surface patterns and spectral screening for Earth candidates. | **Secondary Earth imagery collection.** No thermal infrared band; mask clouds, snow, and invalid pixels using scene-classification/quality assets. |
| `aster-l1t` — ASTER L1T | Microsoft Planetary Computer catalog extent 2000–2006; AST_L1T calibrated at-sensor radiance, with VNIR 15 m, SWIR 30 m, and TIR 90 m bands. This is not surface reflectance or surface temperature. | Optional historical at-sensor radiance context. | **Optional only.** Catalog availability and exact scenes remain unverified. Use separate AST_07/AST_07XT products for surface reflectance or AST_08 for surface kinetic temperature only after verifying access, coverage, and product metadata. ASTER SWIR data acquired since April 2008 are unusable following the SWIR detector failure; VNIR and TIR data continued to function. Check the acquisition date and individual band availability before using ASTER products. ([NASA ASTER SWIR User Advisory](https://asterweb.jpl.nasa.gov/swir-alert.asp)) |
| Copernicus DEM GLO-30 / GLO-90 | Global digital surface model products at 30 m / 90 m; DSM includes vegetation and built structures. | Earth terrain slope, relief, and roughness. | **Preferred first Earth DEM candidate**, subject to checking actual coverage, coordinate metadata, access terms, and the implications of DSM rather than bare-earth elevation. |

| Catalog entry | URL |
|---|---|
| **Microsoft Planetary Computer STAC API:** | <https://planetarycomputer.microsoft.com/api/stac/v1/> |
| Landsat collection: | <https://planetarycomputer.microsoft.com/api/stac/v1/collections/landsat-c2-l2> |
| Sentinel-2 collection: | <https://planetarycomputer.microsoft.com/api/stac/v1/collections/sentinel-2-l2a> |
| ASTER collection: | <https://planetarycomputer.microsoft.com/api/stac/v1/collections/aster-l1t> |
| Copernicus DEM product information: | <https://dataspace.copernicus.eu/explore-data/data-collections/copernicus-contributing-missions/collections-description/COP-DEM> |

### Moon observations — NASA / LRO

| Product / instrument | Published characteristics / access | Intended use | Decision |
|---|---|---|---|
| LRO LOLA LDEM | 20 m/pixel DEM used in the 2026 lunar landing-site study. | Slope, local relief, roughness, terrain morphology, PSR mapping. | **Core lunar terrain input.** |
| LOLA RDR tracks | Individual altimetry measurements; the 2026 study reports ~5 m laser spots and ~10 cm precision along orbital tracks. | Validate or inspect selected detailed profiles; not a uniformly gridded surface. | **Optional validation input.** |
| LRO Diviner polar temperature maps | 240 m/pixel in the 2026 study. | Thermal context for PSRs and volatile-preservation discussion. | **Core context layer**, but not directly comparable to Earth land-surface temperature. |
| LRO WAC / NAC imagery | WAC ~100 m/pixel; south-polar NAC mosaics ~1 m/pixel in the 2026 paper. | Regional and local morphology; visual validation. | **Core imagery/context.** |
| Wueller et al. (2026) derivative files | Zenodo includes landing-site shapefiles, illumination maps, modeled crater-age shapefile, and PSR/volatile shapefile. | Reproduce/validate published analysis and provide known reference geometry. | **Strong starting point**; cite as a derived research dataset, not raw instrument data. |

Sources: <https://doi.org/10.5281/zenodo.17084058> ; <https://imbrium.mit.edu/> ; <https://data.lroc.im-ldi.com/lroc/view_rdr/NAC_POLE_SOUTH> ; <https://pds.nasa.gov/>

### Mars observations — NASA PDS / USGS Astrogeology

| Product / instrument | Published/source characteristics | Intended use | Decision |
|---|---|---|---|
| MOLA MEGDR | Global gridded topography at several map resolutions (including 4, 16, 32, 64, and 128 pixels/degree). | Planetary/regional context and broad elevation setting. | **Core context**, but too coarse for detailed rover-scale roughness at Jezero. |
| CTX stereo DTM | USGS documents a Jezero crater CTX DEM mosaic at 20 m/pixel; individual stereo DTM products and post spacing must be checked for the chosen AOI. | Jezero basin, fan/delta, slope and terrain morphology. | **Preferred regional Mars DTM** if suitable Jezero coverage is available. |
| HiRISE stereo DTM | USGS lists a Mars 2020 Jezero HiRISE DTM mosaic with 1 m posting. This is a product specification, not a guarantee of coverage for every selected Jezero AOI. | Local-scale validation and fine morphology. | **Optional high-resolution validation**, not the only data scale in a cross-body comparison. |
| CRISM | Visible/infrared hyperspectral mapper for Mars surface geology, composition, and layering; the PDS page lists current product records, but a specific 2026 migration/release claim needs a dated release note. | Mineralogical context for Jezero. | **Advanced extension** after checking target coverage, current product version, and processing requirements. |
| THEMIS | Mars Odyssey thermal infrared instrument/data archive. | Thermal/geological context. | **Optional extension**; verify the exact product, local time, season, and Jezero coverage before use. |

Sources: MOLA MEGDR <https://pds-geosciences.wustl.edu/missions/mgs/megdr.html> ; USGS Jezero DTM quality study <https://www.usgs.gov/publications/evaluating-stereo-dtm-quality-jezero-crater-mars-hrsc-ctx-and-hirise-images> ; USGS Jezero CTX mosaic (20 m/pixel) <https://www.usgs.gov/media/images/m20jezerocraterctxdemmosaic20m100jpg> ; USGS Jezero HiRISE DTM product (1 m posting) <https://astrogeology.usgs.gov/search/map/Mars/Mars2020/JEZ_hirise_soc_006_DTM_MOLAtopography_DeltaGeoid_1m_Eqc_latTs0_lon0_blend40> ; CRISM <https://pds-geosciences.wustl.edu/missions/mro/crism.htm> ; NASA PDS releases <https://pds.nasa.gov/datasearch/subscription-service/SS-Release.shtml> ; USGS Astrogeology <https://www.usgs.gov/centers/astrogeology-science-center/science/instruments-data-and-software>.

---

## 6. First MVP scope recommended

Do not attempt every variable or every analog site in the first implementation. A solo project needs one complete, reproducible workflow before expanding.

### MVP-1: two reference tracks, a small benchmark set

**Track A — Moon (proposed):** PNS02 (Peak Near Shackleton) compared with Lake Bonney/McMurdo Dry Valleys and Haughton as *cold/polar field-operation and terrain-context benchmarks*. PNS02 is a provisional scientific reference from the published PNS-region study, not one of the nine regions in NASA's October 2024 updated Artemis III list. The app must explicitly state that neither Earth site reproduces lunar vacuum, gravity, radiation, unshielded thermal cycling, or the lunar day/night cycle.

**Track B — Mars (proposed):** Jezero Crater compared with Atacama salars and Haughton as initial benchmarks; add Lonar for basaltic impact-crater comparison. Lake Bonney and Rio Tinto may appear as specialized cryo-hydrologic and acidic geochemical contrasts, respectively.

### MVP variables

1. Slope distribution from DEMs.
2. Local relief / terrain roughness at fixed physical window sizes.
3. Landform/morphology labels supported by imagery and published geology.
4. Basic Earth surface-reflectance/thermal context from Landsat or Sentinel-2.
5. A provenance and limitations panel for every displayed data layer.

Do **not** create one composite similarity score initially. First show the measured variables side by side. Introduce a weighted score only after we have a documented rationale, validated processing, common spatial scale, explicit missing-data rules, and sensitivity analysis.

### What is deliberately out of scope for MVP-1

- Claiming that an Earth site is a full Moon or Mars replica.
- Estimating water ice reserves from Earth satellite imagery.
- Inferring pH, salinity, mineral abundance, or subsurface biology from optical imagery alone.
- Comparing raw elevation values across planetary bodies without reference-datum treatment.
- Comparing raw spectral band values across unrelated sensors without calibration/bandpass correction.
- Treating land-surface temperature as mean annual air temperature.
- Training a machine-learning model before obtaining a defensible, labelled dataset.

---

## 7. Data audit tasks before download

For each selected AOI, record:

- Exact polygon/coordinate system and source of the region boundary.
- STAC collection and query URL; number of returned scenes/items.
- Acquisition date range, cloud cover, snow/ice/cloud masks, and valid-data fraction.
- Native pixel size, effective spatial resolution, CRS, vertical datum, and units.
- Product version, asset name, source provider, licence/terms, and attribution requirement.
- Any resampling, reprojection, masking, mosaicking, or normalization applied.
- Whether the resulting layer actually supports the variable claimed in the application.

**Global catalog coverage is not proof of usable AOI coverage.** We must query each exact candidate polygon and inspect actual items before claiming a dataset is integrated.

## 8. Key comparability and uncertainty rules

1. **Spatial scale:** Do not upsample a coarse product and call it high-resolution data. Degrade products to a defensible common effective scale for cross-body comparison. State the chosen scale and the reason.
2. **Terrain metrics:** Compare slope distributions, roughness, local relief, and landform shape using a consistent projection and physical window size. Do not compare absolute elevations casually across Earth, Moon, and Mars datums.
3. **Thermal metrics:** Earth Landsat/ASTER, lunar Diviner, and Mars THEMIS observe different bodies with different atmospheric, emissivity, temporal, and viewing conditions. Treat temperature as contextual evidence unless a rigorously harmonized comparison is justified.
4. **Spectral metrics:** Landsat, Sentinel-2, ASTER, CRISM, and lunar instruments have different bandpasses and calibration. Do not equate similarly named bands or raw reflectance values.
5. **Climate:** Published modern Earth climate values do not directly reproduce ancient Martian climate or lunar surface conditions. Use climate as a site descriptor and analog-purpose variable, not an absolute planetary equivalence.
6. **Ground truth:** Geochemistry, pH, salinity, water source, biological signatures, and subsurface structure often require field measurements or mission in-situ observations. Satellite data can guide screening but cannot replace this evidence.
7. **Model uncertainty:** The 2026 lunar study’s PSR ages and volatile quantities are model-derived estimates, not direct confirmation of accessible ice. Show them as published estimates with the paper’s caveats.
8. **Candidate language:** Label new locations as “potential analog candidates” until independent geological/field evidence validates them.

---

## 9. Decisions and open questions

| Item | Current decision | Still to verify |
|---|---|---|
| Lunar reference | PNS02 in Peak Near Shackleton | Confirm lunar coordinate reference and exact PNS02 geometry/Zenodo layer; describe PNS02 as a literature-based provisional reference, not a region in NASA's October 2024 updated Artemis III list. |
| Secondary lunar case | CR05 | Keep secondary because Connecting Ridge was removed from NASA’s 2024 updated candidate-region list. |
| Mars reference | Jezero Crater | Define exact AOI polygon around the science target(s), not simply the broad crater outline. |
| Earth Mars benchmarks | Atacama salars, Haughton, Lonar | Query cloud-free scenes and choose AOI polygons; decide which two fit MVP time. |
| Earth lunar benchmarks | Lake Bonney/McMurdo, Haughton | Verify DEM and satellite coverage at high southern/northern latitudes. |
| Core Earth DEM | Copernicus DEM GLO-30 | Verify exact coverage, DSM implications, and data access/terms for all candidate sites. |
| Core Earth imagery | Landsat C2 L2; Sentinel-2 L2A | Query STAC for each AOI and inspect quality/coverage. Do not treat ASTER L1T at-sensor radiance as surface reflectance. |
| Core lunar inputs | LOLA LDEM + Diviner + LROC; published Zenodo derivative files | Download a small PNS02 subset and validate metadata/CRS/units. |
| Core Mars inputs | MOLA context + CTX DTM; CRISM optional | Verify CTX DTM coverage of selected Jezero AOI and product availability. |
| Scoring | No composite score yet | Establish variables, normalization, weights, sensitivity and missing-data rules only after data audit. |

---

## 10. Key references

1. Wueller, L., Berger, L. M., Christopher, H., Sugimoto, K., Thaker, A. D., Carton, L., et al. (2026). *Assessing Potential Landing Sites With Favorable Illumination and Accessible, Potentially Volatile-Rich Permanently Shadowed Regions Within Artemis Candidate Landing Regions*. Journal of Geophysical Research: Planets, 131, e2025JE009434. <https://doi.org/10.1029/2025JE009434>
2. Sathyan, S., Bhatt, M., Chowdhury, M., Gläser, P., Misra, D., Srivastava, N., Narendranath, S., Sajinkumar, K. S., & Bhardwaj, A. (2024). *Potential landing sites characterization on lunar south pole: De-Gerlache to Shackleton ridge region*. Icarus, 115988. <https://doi.org/10.1016/j.icarus.2024.115988>
3. Harris, C. M., Maclay, M. T., Lutz, K. A., Nathan, V., Ortega Dominguez, N. A., Leavitt, W. D., & Palucis, M. C. (2022). *Remote and in-Situ Characterization of Mars Analogs: Coupling Scales to Improve the Search for Microbial Signatures on Mars*. Frontiers in Astronomy and Space Sciences, 9, 849078. <https://doi.org/10.3389/fspas.2022.849078>
4. NASA (2024). *NASA Provides Update on Artemis III Moon Landing Regions*. <https://www.nasa.gov/news-release/nasa-provides-update-on-artemis-iii-moon-landing-regions/>
5. U.S. Geological Survey (2020). *Evaluating stereo DTM quality at Jezero Crater, Mars with HRSC, CTX, and HiRISE images*. <https://www.usgs.gov/publications/evaluating-stereo-dtm-quality-jezero-crater-mars-hrsc-ctx-and-hirise-images>
6. NASA Planetary Data System — MOLA MEGDRs. <https://pds-geosciences.wustl.edu/missions/mgs/megdr.html>
7. NASA Planetary Data System — CRISM. <https://pds-geosciences.wustl.edu/missions/mro/crism.htm>
8. Microsoft Planetary Computer — Landsat Collection 2 Level-2 STAC collection. <https://planetarycomputer.microsoft.com/api/stac/v1/collections/landsat-c2-l2>
9. Microsoft Planetary Computer — Sentinel-2 Level-2A STAC collection. <https://planetarycomputer.microsoft.com/api/stac/v1/collections/sentinel-2-l2a>
10. Microsoft Planetary Computer — ASTER L1T STAC collection. <https://planetarycomputer.microsoft.com/api/stac/v1/collections/aster-l1t>
11. Copernicus Data Space — Copernicus DEM. <https://dataspace.copernicus.eu/explore-data/data-collections/copernicus-contributing-missions/collections-description/COP-DEM>
12. NASA Space Apps Challenge 2026 — Challenge statement. <https://www.spaceappschallenge.org/2026/challenges/permanent-moon-base-locations-and-mars/?tab=details>
13. NASA ASTER Data Products — AST_L1T at-sensor radiance; AST_07/AST_07XT surface reflectance; AST_08 surface kinetic temperature. <https://asterweb.jpl.nasa.gov/data_products.asp>
14. USGS Astrogeology — Jezero CTX DEM mosaic, 20 m/pixel. <https://www.usgs.gov/media/images/m20jezerocraterctxdemmosaic20m100jpg>
15. USGS Astrogeology — Mars 2020 Jezero HiRISE DTM mosaic, 1 m posting. <https://astrogeology.usgs.gov/search/map/Mars/Mars2020/JEZ_hirise_soc_006_DTM_MOLAtopography_DeltaGeoid_1m_Eqc_latTs0_lon0_blend40>
16. NASA LP DAAC — AST_L1T Quick Reference Guide; SWIR bands are unusable for acquisitions beginning April 2008. <https://lpdaac.usgs.gov/documents/174/AST_L1T_Quick_Reference_Guide.pdf>

---

**Document status:** Preliminary research basis. No LUNA-TERRA scientific results, new analog discoveries, or calculated similarity scores are asserted in this document.
