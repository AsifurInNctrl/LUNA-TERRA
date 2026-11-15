import shapefile
import streamlit as st
import plotly.graph_objects as go
from src.pns02_data import TARGET_IDS, candidates, load_pns02_data, overlap_summary

st.set_page_config(page_title="LUNA-TERRA | PNS02 Evidence Explorer", page_icon="🌑", layout="wide")
st.title("🌑 LUNA-TERRA — PNS02 Evidence Explorer")
st.caption("A source-backed lunar south-pole evidence explorer · NASA Space Apps 2026")
st.markdown("Investigate supplied permanently shadowed region (PSR) polygons around candidate site PNS02. This viewer shows evidence, not confirmed water resources or Earth-analog rankings.")
with st.expander("Research context and status", expanded=True):
    st.write("LUNA-TERRA investigates purpose-specific Earth environments that may inform lunar and Martian exploration. PNS02 is a candidate landing site near the lunar south pole.")
    st.info("Implemented: supplied lunar polygons, CRS transformation, attributes and overlap calculations. Planned: NASA raster integration, terrain measurements and cross-planet comparisons. No similarity score is produced.")
try:
    data = load_pns02_data()
except (OSError, ValueError, shapefile.ShapefileException) as exc:
    st.error(f"Could not load supplied data. Set LUNA_TERRA_RESEARCH_ROOT to the inspection folder. {exc}")
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
c=st.columns(4)
c[0].metric("PSR source polygons",len(data['psr_geoms']))
c[1].metric("Positive-area overlaps",len(rows))
c[2].metric("Area",f"{data['area_geoms'][area_i].area:,.0f} m²")
c[3].metric("CRS transform","Applied" if data['transformed'] else "Not needed")
st.subheader("Interactive lunar spatial explorer")
st.caption(f"Lunar projected X/Y in metres · {data['display_crs'].name}. No Earth basemap or lat/lon display.")
sel=st.selectbox("Inspect PSR feature",range(len(data['psr_attrs'])),format_func=lambda i:f"Id_1={data['psr_attrs'][i].get('Id_1')}"+(" · PNS02 overlap" if int(float(data['psr_attrs'][i].get('Id_1',-1))) in overlap_ids else "")+(" · investigated" if int(float(data['psr_attrs'][i].get('Id_1',-1))) in TARGET_IDS else ""))
fig=go.Figure()
def addpoly(g,name,color,fill,hover,width):
    for p in (list(g.geoms) if g.geom_type=="MultiPolygon" else [g]):
        x,y=p.exterior.xy
        fig.add_trace(go.Scatter(x=list(x),y=list(y),mode="lines",fill="toself",name=name,line={"color":color,"width":width},fillcolor=fill,text=hover,hovertemplate="%{text}<extra></extra>"))
for i,(a,g) in enumerate(zip(data['psr_attrs'],data['psr_geoms'])):
    ident=int(float(a.get('Id_1',-1))); chosen=i==sel; target=ident in TARGET_IDS
    addpoly(g,f"PSR {ident}","#ffc36a" if chosen else ("#e87b62" if target else "#8192a3"),"rgba(255,195,106,.28)" if chosen else ("rgba(232,123,98,.18)" if target else "rgba(129,146,163,.10)"),f"Id_1={ident}<br>meanAge={a.get('meanAge')}<br>Volatiles_={a.get('Volatiles_')}<br>Volatiles1={a.get('Volatiles1')}",2 if chosen else 1)
addpoly(data['area_geoms'][area_i],"PNS02 exploration area","#31c9aa","rgba(49,201,170,.06)","PNS02 exploration area",3)
fig.update_layout(height=600,template="plotly_dark",xaxis_title="Lunar projected X (m)",yaxis_title="Lunar projected Y (m)",yaxis_scaleanchor="x",legend={"orientation":"h"},margin={"t":20,"b":10})
st.plotly_chart(fig,use_container_width=True)
a=data['psr_attrs'][sel]
st.subheader(f"PSR feature inspector · Id_1={a.get('Id_1')}")
st.warning("Original names are preserved. Age and volatile interpretations remain under source-methodology validation; Volatiles_max is not inferred here.")
st.dataframe({k:[a.get(k)] for k in ["Id_1","meanAge","Volatiles_","Volatiles1","Shape_Area"] if k in a},hide_index=True,use_container_width=True)
with st.expander("All source attributes"): st.json(a)
st.subheader("Scientific data quality")
for status,title,detail in [("PASS","Archive provenance","Zenodo checksums match local archives."),("PASS","Geometry inventory",f"{len(data['psr_geoms'])} PSRs loaded; five positive-area overlaps reproduced."),("FAIL","ID 335 association","Workbook point is about 59.8 km from PSR Id_1=335."),("FAIL","Age-field agreement","All five workbook and polygon meanAge pairs differ."),("INCONCLUSIVE","Volatile aggregation","Five-feature sum does not reconcile to the published approximate total.")]:
    with st.container(border=True): st.markdown(f"**{status} · {title}**  \n{detail}")
st.subheader("Provenance and methodology")
st.markdown("[Zenodo DOI 10.5281/zenodo.17084058](https://doi.org/10.5281/zenodo.17084058) · [Wueller et al. 2026 DOI 10.1029/2025JE009434](https://doi.org/10.1029/2025JE009434)\n\nPSR features transform from the source lunar stereographic CRS to the verified exploration CRS with PyProj and explicit x/y order. Intersections use projected metres. Supporting Information S1 indicates where detailed model methods are documented; method verification remains in progress.")
st.caption("No NASA mission observation product is integrated yet. A bounded LOLA RDR topography subset from NASA PDS is the recommended next addition; see docs/data_sources.md.")

st.subheader("Earth Analog Research Roadmap")
st.caption("Proposed benchmark environments from the literature review; these are research targets, not validated analog rankings.")
st.markdown("| Proposed benchmark | Research purpose to investigate |\n|---|---|\n| Atacama Desert | Hyperarid terrain and habitability / instrument-testing context for Mars analog research. |\n| Haughton Impact Crater | Impact geology, polar aridity, and field operations in a cold-desert setting. |\n| Lake Bonney / McMurdo Dry Valleys | Cold-desert hydrology, hypersaline lakes, and microbial extremophile environments. |\n| Lonar Crater | Basaltic impact-crater geology and saline/alkaline lake processes. |\n| Rio Tinto | Acidic, iron-rich water-rock interaction and astrobiology research. |")
st.markdown("**Attribution:** Lunar source vectors are from Wueller et al., *Complementary Data* (Zenodo v1, 2025), CC BY 4.0. Cite Wueller et al. (2026), JGR: Planets, DOI 10.1029/2025JE009434. Local packaged source-file SHA-256 checksums are in `data/demo/pns02/checksums.csv`.")
