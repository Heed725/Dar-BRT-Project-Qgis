# Dar es Salaam BRT — current and future phases

Information snapshot: **9 October 2026**. Designed for QGIS 3.34 and newer, including QGIS 3.40.

## Open the project

1. Extract the entire ZIP into one folder. Do not open the project from inside the ZIP.
2. Open **Dar_BRT_All_Phases.qgz** for the regional network and extensions.
3. Open **Dar_BRT_City_Detail.qgz** for a closer city view.
4. Expand CURRENT or FUTURE in the Layers panel. Tick individual phases to compare them.
5. Offline background maps are included. Internet is only needed for the optional online background layer and source links.

The ZIP also contains an editable GeoPackage, individual phase styles, a CSV phase summary and this guide. The two PNG map previews are available separately in the GitHub repository.

## Status used in the map

| Phase | Status in this project | Main coverage |
|---|---|---|
| 1 | Operating | Kimara–CBD/Kivukoni; Magomeni–Morocco; Fire–Gerezani |
| 2 | Operating | Kilwa/Mbagala; Kawawa South/Changombe; city and port connectors |
| 3 | Construction / commissioning | City–Nyerere Road–Gongo la Mboto; Gerezani–Buguruni–TAZARA branch |
| 4 | Under construction | City–Tegeta/Boko Basihaya; Mwenge–Ubungo branch |
| 5 | Planned / pre-construction | Mandela; Tabata–Segerea; Tabata–Kigogo; Veterinary–Mbagala branch |
| 6 | Planned, subject to review | Mwai Kibaki/Kawe/Lugalo; western and southern extensions |
| 7 | Planning discussion only | No published fixed alignment was identified; no line has been invented |

DART's current background page identifies Phases 1–2 as operating, 3–4 as under construction and 5–6 as preparatory. Phase 2 infrastructure was inaugurated on 7 August 2026. Construction completion is different from the start of passenger operations; Phase 3 is therefore not presented as an operating corridor.

Phase 4 Package 4-1 was reported **65% complete on 1 October 2026**. That percentage refers to one construction package, not the entire phase. The Phase 3 road package is near completion while associated depot/building works extend into 2027. These are project-wide status categories; they do not identify the construction state of every metre of road.

## Accuracy and planning differences

**The coloured lines are approximate corridor reconstructions from published descriptions and OpenStreetMap road geometry. They are not official engineering GIS data, surveyed bus-lane centrelines, or passenger service routes.** City connectors, junctions, road-side selection and endpoints require confirmation against final DART/TANROADS engineering plans before detailed design or operational use.

Selected hubs are place references. The map does not claim to contain every station, platform, depot, feeder service or bus stop. “Airport corridor” marks the nearby road corridor, not a surveyed airport-terminal footprint.

Indicative connectors join gaps between available road extracts. The **connector_m** field records their combined length within each reconstructed segment; these portions need particular attention when replacing the reconstruction with engineering data. Phase 4's northern main corridor contains about 5.8 km of indicative connectors in total, and the Phase 5 Mbagala branch is particularly approximate. Some named-road shapes are supplemented from OSRM's OpenStreetMap-based routing graph. No bus timetable, road-side carriageway assignment or construction-package boundary is inferred from that graph.

Official sources differ on Phase 6's western extent: the phase page names **Kibaha**, while the project-photo overview names **Kibamba**. The project distinguishes the longer **Kibamba–Kibaha** planning option in its own layer. The exact western terminus and detailed alignment remain subject to confirmation. Vikindu is represented by an indicative corridor destination along Kilwa Road, not an approved terminal site.

A 6 October 2026 news report describes a review of Phases 6 and 7, including possible links to Muhimbili and other high-demand destinations. This is retained in the phase summary. No final Phase 7 alignment was available in the consulted material, so it has no spatial line layer.

Published lengths also differ by document and project scope. The CSV and GeoPackage phase summary retain reported values as text. **map_km** measures the reconstructed segment only. Do not sum reported phase lengths repeated on segment rows, or treat reconstructed lengths as official project totals.

## Change colours or labels

- Right-click a phase → Properties → Symbology → change the line colour or width.
- Right-click a phase → Properties → Labels → choose “No labels” to remove its phase labels.
- The selected-hubs layer controls place labels separately.
- Solid lines show operating phases; dashed lines show construction; dash-dot/dotted lines show future corridors.
- The Projects menu → Layouts contains regional and city map layouts, with a north arrow, legend and scale bar.
- View → Panels → Spatial Bookmarks provides regional and city zoom presets.

## Edit and export

Each displayed phase is a filtered view of the shared **corridors** table in **data/Dar_BRT.gpkg**. Editing its geometry or attributes updates that common table. Back up the GeoPackage before editing. Changing only the status field does not automatically move a feature into a different layer group or change the phase's default colour.

To export one phase, right-click its layer → Export → Save Features As. Choose GeoPackage, GeoJSON, Shapefile or KML. The source data is WGS 84 (EPSG:4326); the project uses UTM zone 37S (EPSG:32737) for metre-based mapping. The offline background rasters use EPSG:3857 and QGIS transforms them automatically.

## Sources and attribution

See **sources.csv** for links, publication dates when known and how each source was used. Dates on undated website pages are access dates rather than publication dates. No opening date or completion date has been inferred merely because an earlier forecast has passed.

- DART: current status, corridor descriptions, programme and procurement documents.
- TANROADS: dated construction progress.
- The Citizen: September/October 2026 reporting on Phase 5 and the Phase 6/7 planning review.
- Road geometry: **© OpenStreetMap contributors**, distributed under **ODbL 1.0**. https://www.openstreetmap.org/copyright and https://opendatacommons.org/licenses/odbl/1-0/
- Offline background: **Esri World Street Map and its contributors**. Attribution and service information: https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer

This is an independent reference map; it is not an official DART publication. Source dates and indicative geometry are retained so the project can be updated when authoritative alignments and operating notices become available.
