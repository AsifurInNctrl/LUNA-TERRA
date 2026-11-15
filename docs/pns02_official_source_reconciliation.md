# PNS02 official source reconciliation

Date: 2026-11-15

## Executive summary

The local `PSR_Volatile_Estimates.zip`, `Landing_Sites.zip`, and crater-age workbook are byte-for-byte identical to the corresponding files listed in the official Zenodo v1 record: each local MD5 matches the Zenodo MD5. The locally extracted PSR and landing-site layers are present and their records/attributes reproduce the previously observed results. Zenodo explicitly documents `Volatiles_max` as the volatile estimate field; the local DBF uses 10-character shapefile names `Volatiles_` and `Volatiles1`. The ArcGIS layer file is the source of aliases to check for this mapping; interpreting the DBF names as separate lower/upper bounds is supported by paper text and numerical examples, but field-alias binding should be verified against official layer metadata. The published paper states the PNS02 cumulative amount is about 150,000 kg over five PSRs. Simple sum of all five `Volatiles1` values is 222,434.85; four features excluding ID 338 sum to 150,540.51. The article describes five craters in the exploration zone and gives the 250 m PSR as 7,750–15,550 kg; this four-feature coincidence does not establish that excluding 338 is the correct published method. The local workbook and polygon layer are official-identical, but ID 335's workbook center remains ~59.8 km from its PSR polygon, unresolved in official records. Do not repair the ID join.

## Official inventory and byte comparison

Zenodo record 17084058, version v1 (published 2025-09-15), describes landing-site geometries, crater-age workbook, and accessible PSR volatile shapefile. Its file table provides MD5 checksums:

| Official file | Zenodo MD5 | Local file | Local MD5 | Result |
|---|---|---|---|---|
| `PSR_Volatile_Estimates.zip` (43.9 kB) | `30bc10b0bd1c772afbdd606b3e920942` | `Downloads\PSR_Volatile_Estimates.zip` | `30bc10b0bd1c772afbdd606b3e920942` | PASS, byte-identical archive |
| `Landing_Sites.zip` (11.9 MB) | `fdd66337acc737beff5ce56cfd2b50c0` | `Downloads\Landing_Sites.zip` | `fdd66337acc737beff5ce56cfd2b50c0` | PASS, byte-identical archive |
| `Diffusion_Modeling_Crater_Ages_Soderblom.xlsx` (19.9 kB) | `c138fcd112e1e336c903807df468aadb` | Downloads workbook and inspection-workspace copy | `c138fcd112e1e336c903807df468aadb` | PASS, byte-identical; copies also match each other |

The hashes were calculated locally with PowerShell `Get-FileHash -Algorithm MD5`; Zenodo checksums are from the record file table. Because archive bytes match, their compressed content is identical to official archives. Local extraction contents are compared to the exact archive sources by extraction provenance, but no independent full member-by-member re-extraction checksum manifest was generated in this audit. The archive listings contain nested items named `PSR_Volatile_Estimates.zip` and `Landing_Sites.zip` plus `.lyrx` sidecars; these are as shipped in the Zenodo archives, not evidence of corruption.

Local PSR extracted files: `Downloads\LUNA-TERRA_PNS02_inspection\PSR_Volatile_Estimates\PSR_volatile_abundance_final.{shp,shx,dbf,prj,cpg}`, layer file `PSR_Volatile_Estimates.lyrx`. Local landing site extracted files are in `...\Landing_Sites\` including `LandingSites` and `ExplorationArea_2km` shapefile sidecars. Extracted schema/geometry previously inspected by pyshp/Shapely: PSR=141 polygon features; no invalid geometries; PNS02 exploration area `BUFF_DIST=2000`, projected area 12,565,537.34 m². PSR and exploration CRS differ and were transformed before overlay. Archive identity is strong evidence of provenance; no separate version drift was found.

## Field names and volatile estimates

Zenodo states the PSR attribute-table estimate is `Volatiles_max`. Shapefile DBF field names are limited to 10 characters, so the likely DBF counterpart is `Volatiles1` (10 chars) while `Volatiles_` is another separately stored field; however truncation by itself cannot prove aliases. The full `.lyrx` JSON should be checked for `fieldName`/`alias` bindings. The scientific article independently calls the values upper and lower estimates and reports 7,750 to 15,550 kg for the nearby ID 325 PSR, matching `Volatiles_`=7,765.7655 and `Volatiles1`=15,559.2054 to rounding. This supports mapping `Volatiles_` → lower and `Volatiles1` → upper/Zenodo `Volatiles_max` (PASS at the ID 325 published-example level; definitive alias mapping via layer metadata remains a verification item).

`Volatiles_max` estimates use net delivery minus sublimation/loss rate multiplied by crater modeled age; units of rate are kg km⁻² Ma⁻¹ and age is Ma, yielding kg. Main paper §6.3 describes upper and lower literature-flux estimates and cautions these are modeled potential abundances, not direct evidence of volatiles. S1 is cited as the detailed source for topographic diffusion and volatile sublimation methods. The Zenodo field alone does not encode uncertainty semantics beyond the documented upper estimate.

| PSR Id_1 | `Volatiles_` (likely lower, kg) | `Volatiles1` (likely max, kg) | Exploration overlap | Status |
|---:|---:|---:|---:|---|
| 325 | 7,765.7655 | 15,559.2054 | 100% | PASS; article's 7,750–15,550 kg example |
| 330 | 19,114.8479 | 38,297.3761 | 100% | PASS values reproduced; feature-level paper cross-check not located |
| 335 | 1,596.2483 | 3,198.1485 | 100% | INCONCLUSIVE object association (see below) |
| 324 | 46,660.2859 | 93,485.7827 | 71.1328% | PASS values reproduced; clipping rule not stated in attributes |
| 338 | 35,883.6441 | 71,894.3422 | 0.6755% | PASS values reproduced; inclusion/matching rule needs explanation |
| **five-feature sum** | **111,020.7917** | **222,434.8550** | n/a | PASS arithmetic, FAIL as direct reproduction of published PNS02 total |
| **four-feature sum excluding 338** | **75,137.1476** | **150,540.5127** | n/a | PASS arithmetic, INCONCLUSIVE published methodology |

The published approximate ∼150,000 kg agrees numerically with the four-feature upper bound excluding ID 338, while paper prose says PNS02 has five PSR-hosting craters in the exploration zone. It would be unsound to infer the fifth is excluded solely from the sum. The source layer labels 338 as a polygon with only 120.76 m² positive overlap, but its PSR ID is among the five matches and the full polygon maximum is 71,894 kg. A legitimate clipped estimate would require re-running the paper's spatial and model calculations on the clipped geometry, including its temperature, crater age, and flux assumptions; scaling the full feature estimate by polygon overlap is not justified without evidence of uniform areal density and identical PSR boundary semantics. No independent spatially clipped volatile recalculation is claimed here.

## Crater 335 and identifiers

Official Zenodo workbook is byte-identical to the local file. The verification script reads workbook `Id`, `Latitude`, and `Longitude`; it joins by numeric ID to shapefile `Id_1`. Coordinate parsing accounts for S/W signs, and `pyproj` transforms lon/lat using the geographic CRS derived from the lunar PSR `.prj` into the PSR's Moon_2000_South_Pole_Stereographic CRS (metres, lunar datum/radius), with explicit x/y order. It is not an Earth EPSG conversion. Independent check of exact records: workbook ID 335 = -88.737914°, -109.246494°; corresponding PSR `Id_1=335` center is 59,838.19 m from polygon, centroid distance 59,867.00 m. This exceeds both 2 km site association context and local polygon scale. The PSR itself overlaps the PNS02 exploration area but that does not prove crater-center identity. Official archive checks rule out a local-version mismatch. Current evidence therefore fails a spatially verified ID 335 association; whether it is a non-spatial cross-reference, source data mismatch, or different object definition is inconclusive. Do not alter coordinate or ID.

## Crater age field reconciliation

Zenodo describes workbook `meanAge` as modeled crater age for PSR-hosting craters within 2 km of candidate landing sites. Workbook fields include `Id`, coordinates, `Diameter`, `meanAge`, `errAge`, `meanAge_dD`, `errAge_dD`, `meanAge_dep`, `errAge_dep`. PSR polygon DBF has `Id_1` and `meanAge`. Byte identity confirms the workbook values are official. Direct-join values:

| Id | Workbook meanAge | PSR polygon meanAge | Exact match? | Coordinate relation | Assessment |
|---:|---:|---:|---|---|---|
| 325 | 616.25 | 1,445 | No | inside | Values are official but fields not reconciled |
| 330 | 968.75 | 1,593.75 | No | inside | Values are official but fields not reconciled |
| 335 | 565 | 1,425 | No | 59.8 km away | ID association questionable |
| 324 | 2,118.75 | 3,187.5 | No | 6.31 m boundary distance | Values are official but fields not reconciled |
| 338 | 1,400 | 2,387.5 | No | inside | Values are official but fields not reconciled |

The shapefile field name `meanAge` does not establish it has the same modeled age definition as workbook `meanAge`; Zenodo identifies the workbook as the table of modeled ages, while polygon `meanAge` provenance/meaning is not explained in the record description. Published text summarizes PNS02 ages as roughly 1.45–3.2 Ga for five craters, consistent with PSR polygon means for four plus another? But workbook values are different. The article methods say topographic diffusion-derived age; exact table/feature crosswalk and field semantics should be extracted from S1/source project before choosing a canonical field. No direct scientifically valid age reconciliation is established.

## Supporting Information S1 and method

Publisher article and its Data Availability Statement state that S1 contains details on the topographic diffusion model and volatile-loss-by-sublimation estimation. Main article §6.3 states each upper/lower estimate is (volatile influx minus loss rate) × modeled crater age; rate units kg km⁻² Ma⁻¹ times Ma and area handling must be considered to obtain kg. S1 itself was identified on Wiley as `2025JE009434-sup-0001-Supporting Information SI-S01.docx` (1.2 MB), but its full document contents and equations were not extracted in this local audit. Consequently detailed assumptions/uncertainties requested for S1 are INCONCLUSIVE here and must not be filled in from inference. See source links below.

## Published versus reproduced result

Published main-text result: PNS02 cumulative abundance approximately 150,000 kg across five PSR-hosting craters; per-PSR example: nearby 6,800 m², ~1.45 Ga, 91 K PSR yields 7,750–15,550 kg. Reproduced local attribute arithmetic: five max values 222,434.855; four max values excluding 338 150,540.513. The official-source identity passes. The arithmetic discrepancy is real; the exact spatial selection/aggregation that yields the published five-crater total is not yet reproduced. Thus published-result reproduction: INCONCLUSIVE, not PASS.

## Test status and open questions

- PASS — local ZIP and workbook checksums match Zenodo record checksums.
- PASS — local workbook copies identical; source attribute values reproduce.
- PASS — ID 325 lower/upper values agree with published rounded example.
- FAIL — naive full-feature five-PSR `Volatiles_max` sum reproduces ∼150,000 kg (it yields 222,435 kg).
- INCONCLUSIVE — published inclusion/clipping/aggregation rule that results in ∼150,000 kg.
- INCONCLUSIVE — definitive DBF-to-long alias mapping absent decoded `.lyrx` binding; likely `Volatiles1` is max supported by numeric cross-check.
- FAIL — ID 335 workbook center spatially coincides with PSR polygon `Id_1=335`.
- INCONCLUSIVE — nature of ID 335 association and source cause.
- FAIL — workbook and PSR DBF `meanAge` values match for the five IDs; none match.
- INCONCLUSIVE — whether PSR DBF `meanAge` is alternate model measure or metadata error; precise age uncertainty, model assumptions, crater correspondence, and S1 details.
- INCONCLUSIVE — volatile field negative values and what range/quality handling means; no negative-value rule applied.

## Sources

- Zenodo record v1 and file checksums: https://doi.org/10.5281/zenodo.17084058 (record https://zenodo.org/records/17084058).
- Wueller et al. (2026), *Journal of Geophysical Research: Planets*, 131(3), e2025JE009434: https://doi.org/10.1029/2025JE009434. Main paper §6.3 and Data Availability Statement; supporting info filename above.
- Supporting Information S1, DOI-associated Wiley supplementary file: https://agupubs.onlinelibrary.wiley.com/doi/10.1029/2025JE009434.

No local source data, scripts, project application/docs, dependencies, or Git history were modified. Report only was added at the requested location.
