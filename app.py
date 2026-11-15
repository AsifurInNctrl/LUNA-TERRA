import json
import shapefile
import streamlit as st
import plotly.graph_objects as go
from src.pns02_data import (TARGET_IDS, candidates, load_pns02_data, overlap_summary,
                            default_psr_record, default_selection_label, ordered_psr_records,
                            pns02_site_candidates, viewport_bounds)
from src.nasa_site07 import DEFAULT_PACKAGE_DIR as NASA_SITE07_PACKAGE, load_packaged_summary
from src.earth_analog_evidence import DIMENSIONS as ANALOG_DIMENSIONS, EARTH_ANALOGS, STATUS as ANALOG_STATUS

st.set_page_config(page_title="LUNA-TERRA | PNS02 Evidence Explorer", page_icon="🌑", layout="wide")
st.title("🌑 LUNA-TERRA — PNS02 Evidence Explorer")
st.caption("A source-backed lunar south-pole evidence explorer · NASA Space Apps 2026")
st.markdown("Investigate supplied permanently shadowed region (PSR) polygons around candidate site PNS02. This viewer shows evidence, not confirmed water resources or Earth-analog rankings.")
with st.expander("Research context and status", expanded=True):
    st.write("LUNA-TERRA investigates purpose-specific Earth environments that may inform lunar and Martian exploration. PNS02 is a candidate landing site near the lunar south pole.")
    st.info("Implemented: PNS02 vector evidence, a separate NASA LOLA Site07 terrain product summary, and a literature-grounded Earth analog research matrix. The NASA raster is not registered to PNS02; Earth/Mars quantitative comparisons remain proposed. No similarity score or candidate ranking is produced.")
try:
    data = load_pns02_data()
except (OSError, ValueError, shapefile.ShapefileException) as exc:
    st.error(f"Could not load the packaged demo data from data/demo/pns02/. Check the tracked shapefile components. {exc}")
    st.stop()
choices = candidates(data)
if not choices:
    st.error("No exploration-area feature has Name=PNS02; inspect source candidates below.")
    st.dataframe(data["area_attrs"]); st.stop()
if len(choices) == 1:
    area_i = choices[0]
    st.caption(f"Selected by source Name=PNS02, feature {area_i}; ORIG_FID={data['area_attrs'][area_i].get('ORIG_FID')}.")
else:
    area_i = st.selectbox("PNS02 area candidate", choices)
    st.dataframe([data['area_attrs'][i] for i in choices])
rows = overlap_summary(data, area_i)
overlap_ids = {int(float(r['Id_1'])) for r in rows}
overlap_records = {r['source_record'] for r in rows}
c=st.columns(4)
c[0].metric("PSR source polygons",len(data['psr_geoms']))
c[1].metric("Positive-area overlaps",len(rows))
c[2].metric("Area",f"{data['area_geoms'][area_i].area:,.0f} m²")
c[3].metric("CRS transform","Applied" if data['transformed'] else "Not needed")
st.subheader("Interactive lunar spatial explorer")
st.caption(f"Lunar projected X/Y in metres · {data['display_crs'].name}. No Earth basemap or lat/lon display.")
view_mode = st.radio("Map view", ["PNS02 focus", "All PSRs"], horizontal=True,
                     help="The PNS02 focus margin is for display only; it does not change intersections.")
st.caption(f"Active view: **{view_mode}**. Default selection is for inspection only; it does not indicate suitability or priority.")
ordered_records = ordered_psr_records(data, area_i)
default_i = default_psr_record(data, area_i) if rows else ordered_records[0]
if not rows:
    st.warning("No PSR polygons have a positive-area intersection with this exploration area.")
sel_record = st.selectbox(
    "Inspect PSR source record", ordered_records, index=ordered_records.index(default_i),
    format_func=lambda i: default_selection_label(data, i)
        + (" · PNS02 overlap" if data['psr_source_records'][i] in overlap_records else "")
        + (" · investigated" if int(float(data['psr_attrs'][i].get('Id_1', -1))) in TARGET_IDS else ""))
sel = sel_record
fig=go.Figure()
def addpoly(g,name,color,fill,hover,width):
    for p in (list(g.geoms) if g.geom_type=="MultiPolygon" else [g]):
        x,y=p.exterior.xy
        fig.add_trace(go.Scatter(x=list(x),y=list(y),mode="lines",fill="toself",name=name,line={"color":color,"width":width},fillcolor=fill,text=hover,hovertemplate="%{text}<extra></extra>"))
for i,(a,g) in enumerate(zip(data['psr_attrs'],data['psr_geoms'])):
    ident=int(float(a.get('Id_1',-1))); chosen=i==sel; target=ident in TARGET_IDS
    addpoly(g,f"PSR {ident}","#ffc36a" if chosen else ("#e87b62" if target else "#8192a3"),"rgba(255,195,106,.28)" if chosen else ("rgba(232,123,98,.18)" if target else "rgba(129,146,163,.10)"),f"Id_1={ident}<br>meanAge={a.get('meanAge')}<br>Volatiles_={a.get('Volatiles_')}<br>Volatiles1={a.get('Volatiles1')}",2 if chosen else 1)
addpoly(data['area_geoms'][area_i],"PNS02 exploration area","#31c9aa","rgba(49,201,170,.06)","PNS02 exploration area",3)
site_matches = pns02_site_candidates(data, area_i)
if len(site_matches) == 1:
    si = site_matches[0]
    point = data['site_geoms'][si]
    fig.add_trace(go.Scatter(x=[point.x], y=[point.y], mode="markers+text", text=["PNS02 landing-site reference"],
        textposition="top center", name="PNS02 landing-site reference point",
        marker={"size":13,"color":"#f4e04d","symbol":"star","line":{"color":"#111923","width":1}},
        hovertemplate=(f"PNS02 landing-site reference<br>Source record {si + 1}<br>source ID={data['site_attrs'][si].get('ID')}<extra></extra>")))
else:
    st.warning(f"PNS02 point not shown: expected exactly one Name=PNS02 point covered by the selected exploration geometry; found {len(site_matches)}.")
if view_mode == "PNS02 focus":
    xmin, xmax, ymin, ymax = viewport_bounds(data['area_geoms'][area_i], 0.1)
else:
    xmin = min(g.bounds[0] for g in data['psr_geoms'])
    ymin = min(g.bounds[1] for g in data['psr_geoms'])
    xmax = max(g.bounds[2] for g in data['psr_geoms'])
    ymax = max(g.bounds[3] for g in data['psr_geoms'])
fig.update_layout(height=700,template="plotly_dark",xaxis_title="Lunar projected X (m)",yaxis_title="Lunar projected Y (m)",
    xaxis={"range":[xmin,xmax]}, yaxis={"range":[ymin,ymax],"scaleanchor":"x","scaleratio":1},
    legend={"orientation":"h"},margin={"t":20,"b":10})
st.plotly_chart(fig,width="stretch")
a=data['psr_attrs'][sel]
st.subheader(f"PSR feature inspector · Id_1={a.get('Id_1')}")
st.caption(f"Original PSR source record: {data['psr_source_records'][sel]} (1-based source row order).")
st.warning("Original names are preserved. Age and volatile interpretations remain under source-methodology validation; Volatiles_max is not inferred here.")
st.dataframe({k:[a.get(k)] for k in ["Id_1","meanAge","Volatiles_","Volatiles1","Shape_Area"] if k in a},hide_index=True,width="stretch")
with st.expander("All source attributes"): st.json(a)
if len(site_matches) == 1:
    si = site_matches[0]
    st.caption(f"PNS02 landing-site reference point: source record {si + 1}, source ID={data['site_attrs'][si].get('ID')}. It is uniquely selected by Name=PNS02 and lies within the selected PNS02 exploration geometry; this is not evidence of suitability or a confirmed operational landing position.")
st.subheader("Scientific data quality")
for status,title,detail in [("PREPARATION VERIFIED","Source provenance documented; original archives checksum-verified during preparation.","See data/demo/pns02/PROVENANCE.md and checksums.csv. At runtime, the app does not recompute SHA-256 hashes, contact Zenodo, or verify each file against the manifest."),("PASS","Geometry inventory",f"{len(data['psr_geoms'])} PSRs loaded; five positive-area overlaps reproduced."),("FAIL","ID 335 association","Workbook point is about 59.8 km from PSR Id_1=335."),("FAIL","Age-field agreement","All five workbook and polygon meanAge pairs differ."),("INCONCLUSIVE","Volatile aggregation","Five-feature sum does not reconcile to the published approximate total.")]:
    with st.container(border=True): st.markdown(f"**{status} · {title}**  \n{detail}")
st.subheader("Provenance and methodology")
st.markdown("[Zenodo DOI 10.5281/zenodo.17084058](https://doi.org/10.5281/zenodo.17084058) · [Wueller et al. 2026 DOI 10.1029/2025JE009434](https://doi.org/10.1029/2025JE009434)\n\nPNS02 vectors are evaluated separately using their supplied lunar projected CRSs and explicit x/y order. The NASA Site07 section is an independent product-level summary and is not spatially joined to PNS02. Supporting Information S1 indicates where detailed model methods are documented; method verification remains in progress.")

st.divider()
st.subheader("Independent NASA LOLA Site07 terrain evidence")
st.warning("Independent NASA Site07 product. Not spatially registered to the LUNA-TERRA PNS02 exploration polygon.")
st.caption("This section summarizes the complete native NASA Site07 tile only. It does not describe or sample PNS02.")
try:
    nasa = load_packaged_summary()
except (OSError, ValueError, json.JSONDecodeError) as exc:
    st.error(f"Could not load the packaged NASA Site07 derived evidence from data/demo/nasa_site07/. {exc}")
else:
    elevation, slope = nasa["elevation"], nasa["slope"]
    site_cols = st.columns(4)
    site_cols[0].metric("Site07 grid cells", f"{elevation['total_pixel_count']:,}")
    site_cols[1].metric("Surface median", f"{elevation['median']:.2f} m")
    site_cols[2].metric("Slope median", f"{slope['median']:.2f}°")
    site_cols[3].metric("NoData cells (height / slope)", f"{elevation['nodata_or_nonfinite_pixel_count']:,} / {slope['nodata_or_nonfinite_pixel_count']:,}")
    st.markdown("[NASA GSFC PGDA Product 78](https://pgda.gsfc.nasa.gov/products/78) · [Barker et al. (2021)](https://doi.org/10.1016/j.pss.2020.105119)")
    st.caption("Source: Site07, ‘Peak near Shackleton’; elevation is surface height in metres and slope is degrees. NASA product documentation reports extensive interpolation in the 5 m polar DEMs. No LDEC or uncertainty raster was downloaded, so the Site07-specific observed/interpolated fraction and uncertainty are not calculated.")

    map_cols = st.columns(2)
    for col, image_name, label, stats, unit in (
        (map_cols[0], "site07_surface_native_grid.png", "Site07 surface height", elevation, "m"),
        (map_cols[1], "site07_slope_native_grid.png", "Site07 slope", slope, "degrees"),
    ):
        with col:
            st.markdown(f"**{label}**")
            st.image(str(NASA_SITE07_PACKAGE / image_name), width="stretch")
            st.caption(f"Native 3,200 × 3,200 pixel grid; source rows/columns, no resampling or reprojection. Linear display stretch: {stats['minimum']:.2f}–{stats['maximum']:.2f} {unit}.")

    chart_cols = st.columns(2)
    for col, label, stats, units, color in (
        (chart_cols[0], "Full-tile surface-height distribution", elevation, "m", "#edb76a"),
        (chart_cols[1], "Full-tile slope distribution", slope, "degrees", "#55c3b2"),
    ):
        centers = [(a + b) / 2 for a, b in zip(stats["histogram_edges"][:-1], stats["histogram_edges"][1:])]
        widths = [b - a for a, b in zip(stats["histogram_edges"][:-1], stats["histogram_edges"][1:])]
        fig_hist = go.Figure(go.Bar(x=centers, y=stats["histogram_counts"], width=widths,
                                   marker_color=color, hovertemplate=f"{units}: %{{x:.2f}}<br>Pixels: %{{y:,}}<extra></extra>"))
        fig_hist.update_layout(title=label, template="plotly_dark", height=330,
                               xaxis_title=units, yaxis_title="Source pixel count", margin={"t": 45, "b": 30})
        col.plotly_chart(fig_hist, width="stretch")

    st.markdown("**Slope bands across the complete Site07 tile**")
    st.dataframe(nasa["slope_broad_intervals"], hide_index=True, width="stretch")
    with st.expander("Statistics and processing details"):
        st.markdown("Statistics use every finite, unmasked float32 source cell. Percentiles use NumPy's linear quantile method; standard deviation is population standard deviation. The downloaded surface and slope products share CRS metadata, exact affine transform, dimensions, bounds, pixel size, and validity mask. Row/column comparison is valid within this NASA product; no cross-source spatial join is performed.")
        st.json({"surface": elevation, "slope": slope, "grid_alignment": nasa["grid_alignment"], "provenance": nasa["provenance"]})
    st.caption("Raw GeoTIFFs stay outside the repository. The app loads precomputed summaries and full-resolution native-grid visualizations; it does not rehash files at runtime. Processing code and source/output checksums are documented in data/demo/nasa_site07/PROVENANCE.md and checksums.csv.")

st.subheader("Earth Analog Evidence Matrix")
st.caption("Literature-supported research candidates — not yet quantitatively assessed by LUNA-TERRA. These are process-specific research contexts, not site-suitability findings.")
st.info("Literature support is separated from project interpretation and proposed future measurements. A citation is not a direct LUNA-TERRA analysis; no composite score or candidate ranking is calculated.")
matrix_rows = [{
    "Earth candidate": candidate["name"],
    "Primary research relevance": candidate["purpose"],
    "Planetary target/process": candidate["planetary_target"],
    "Evidence source": "; ".join(source["label"] for source in candidate["sources"][:2]),
    "Major limitation": candidate["limitations"][0],
} for candidate in EARTH_ANALOGS]
st.dataframe(matrix_rows, hide_index=True, width="stretch")
st.caption("Comparison dimensions used as an organizing framework (not scores): " + " · ".join(ANALOG_DIMENSIONS.values()))
for candidate in EARTH_ANALOGS:
    with st.expander(candidate["name"]):
        st.markdown(f"**Status:** {ANALOG_STATUS}")
        st.markdown(f"**Research purpose:** {candidate['purpose']}")
        st.markdown(f"**Planetary target/process:** {candidate['planetary_target']}")
        st.markdown("**Relevant dimensions:** " + ", ".join(ANALOG_DIMENSIONS[key] for key in candidate["dimensions"]))
        st.markdown("**Published evidence**  \n" + candidate["evidence"])
        st.markdown("**LUNA-TERRA interpretation**  \n" + candidate["interpretation"])
        st.markdown("**What this analogy does not represent**")
        for limitation in candidate["limitations"]:
            st.markdown(f"- {limitation}")
        st.markdown("**Additional observations needed for quantitative comparison**  \n" + candidate["data_needed"])
        st.markdown("**Sources**")
        for source in candidate["sources"]:
            st.markdown(f"- [{source['label']}]({source['url']}) · {source['kind']}")
        extension = candidate.get("supporting_extension")
        if extension:
            st.markdown(f"**Supporting extension — {extension['name']}**")
            st.markdown(extension["purpose"])
            st.markdown(f"**Evidence:** {extension['evidence']}")
            st.markdown(f"**Boundary:** {extension['limitation']}")
            st.markdown(f"**Source:** [{extension['source']['label']}]({extension['source']['url']})")
st.markdown("**Attribution:** Lunar source vectors are from Wueller et al., *Complementary Data* (Zenodo v1, 2025), CC BY 4.0. Cite Wueller et al. (2026), JGR: Planets, DOI 10.1029/2025JE009434. Local packaged source-file SHA-256 checksums are in `data/demo/pns02/checksums.csv`.")
