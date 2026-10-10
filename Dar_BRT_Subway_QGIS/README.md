# Dar es Salaam BRT — subway-style QGIS schematic

Information snapshot: **9 October 2026**. Created for QGIS 3.34 or newer, including QGIS 3.40.

## Open

1. Extract the entire ZIP into one folder.
2. Open **Dar_BRT_Subway_Schematic.qgz**.
3. Keep the **data** folder beside the project. No internet or background tiles are required.
4. Expand CURRENT or FUTURE in the Layers panel to switch phases on and off.

The map uses straight lines, 45° bends, phase number badges and selected hub circles. It includes an editable GeoPackage, phase styles, an A3 portrait print layout, a PNG preview, the original corridor GeoJSON for reference and source/phase CSVs.

## What the map shows

| Phase | Status retained from the original project | Main coverage |
|---|---|---|
| 1 | Operating | Kimara, Ubungo, Magomeni, Morocco, Fire, Gerezani and Kivukoni |
| 2 | Operating | Kilwa/Mbagala, Kawawa South/Changombe and city/port connectors |
| 3 | Construction / commissioning | Nyerere Road, airport corridor, Gongo la Mboto and Buguruni branch |
| 4 | Under construction | Morocco, Mwenge, Lugalo, Tegeta/Boko Basihaya and Ubungo branch |
| 5 | Planned / pre-construction | Mandela, Tabata, Segerea, Kigogo and the Mbagala branch |
| 6 | Planned / under review | Kawe/Lugalo, western extension and Vikindu extension |
| 7 | Planning note only | No fixed alignment was identified, so no route is drawn |

Solid coloured lines indicate operating phases; dashed lines indicate construction; dash-dot lines indicate planned phases. The lighter dotted Kibamba–Kibaha line is the longer Phase 6 planning option. Published descriptions differ between Kibamba and Kibaha, and the western terminus remains subject to confirmation.

**This is a schematic corridor diagram, not a passenger route map, official station map or engineering alignment.** It adapts the 21 reconstructed segments from the original geographic project into 36 editable diagram parts. Positions and distances are deliberately distorted. The information snapshot has not been refreshed by this visual redesign.

There are 30 selected place/corridor references. Smaller circles mark a selected place or endpoint; larger circles mark a reference shared by multiple phase corridors. A large circle does **not** confirm an operational passenger interchange, a shared platform or through service. Crossings without a circle do not indicate a transfer. Intermediate references such as City junction and the connection to the Mbagala branch are illustrative interpretations of the reconstructed corridors, requiring confirmation from engineering/service plans. The airport symbol marks the nearby road corridor, not an airport terminal.

## Coordinates and geographic use

The project and GeoPackage use a **local engineering CRS named “Dar BRT schematic grid (not geographic)”**. The coordinates are diagram positions, not longitude/latitude or UTM positions. Do not use them for distances, navigation, route lengths, buffers, engineering or basemap overlays, or relabel them EPSG:4326.

For geographic use, open the original **Dar_BRT_All_Phases.qgz** or **Dar_BRT_City_Detail.qgz** in the parent GitHub repository. Those retain the approximate OSM-based geographic corridors and offline backgrounds. The included **data/source_corridors.geojson** is that WGS 84 geographic reconstruction, retained as provenance; it is not displayed in this diagram project. It carries the original source URLs, connector lengths and accuracy notes. Both forms remain independent reference maps, not official DART publications.

## Edit colours and labels

- Right-click a phase → Properties → Symbology. The ordinary and parallel shared-run rules control the colour, thickness and line pattern. Update both rules when changing a phase colour.
- Phase number badges use a separate phase-category renderer. Change the matching badge colour there too.
- The **Selected hubs and place references** layer controls names, circles and text. Edit the **name** field to rename a label. **shared** changes the small/large circle category.
- **label_dx** and **label_dy** are label offsets in diagram units. **halign** accepts Left, Center or Right. Labels follow their point if it is moved.
- To hide names: layer Properties → Labels → No labels.

Each phase is a filtered view of **schematic_corridors** in **data/Dar_BRT_Subway.gpkg**. Use the Vertex Tool to move bends; keep horizontal, vertical or 45° segments for the subway look. Move any associated hub point to the same coordinate when moving a junction. Parallel green/red Buguruni–TAZARA runs have a symbol offset rather than different geographical alignments. If a shared route is changed, update both matching features. Changing only a status field does not automatically change the layer grouping or line pattern.

Back up the GeoPackage before editing. The rebuild script recreates its data and styles, so run it only when the project is closed and after saving a backup of any manual edits.

## Export a map

Project → Layouts → **Dar BRT | Subway schematic** opens the A3 portrait layout. Use Export as Image, PDF or SVG. The supplied preview matches this layout. A scale bar and north arrow are omitted because the diagram has no geographic scale or georeferenced orientation.

## Rebuild

**rebuild_subway_map.py** contains the complete diagram definition and PyQGIS build code. It requires a Python interpreter with QGIS installed, not ordinary Python alone. Its output folder is the folder containing the script. Edit **NODES** for reference positions and labels and **ROUTES** for bends. Each original segment ID is retained. Coordinates must form horizontal, vertical or 45° legs; the script checks this before exporting.

Example on a system where the default Python interpreter has QGIS bindings:

```bash
python3 rebuild_subway_map.py
```

On Windows use the Python environment bundled with your QGIS installation. Opening the finished project does not require running the script.

## Sources and attribution

See **sources.csv**, **phase_summary.csv**, the source GeoJSON and the original project's guide for dated evidence, reported lengths, construction-package qualifications and planning differences. The diagram adds no new assertion that a construction phase has opened.

- Programme status and descriptions: DART, TANROADS and the dated reporting listed in sources.csv.
- Original geographic reconstruction: © OpenStreetMap contributors, [ODbL 1.0](https://www.openstreetmap.org/copyright).
- Diagram layout: a manual schematic adaptation of that reference project.
- No street basemap is included in the schematic package.

Sources retain their respective attribution and licence requirements.
