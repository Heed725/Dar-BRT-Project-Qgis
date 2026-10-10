"""Build the Dar BRT schematic with PyQGIS 3.34+.

Run using a Python interpreter bundled with QGIS. Edit NODES and ROUTES to
adjust diagram positions. Coordinates are local diagram units, not geography.
"""
import os
import json
from pathlib import Path

os.environ.setdefault('QT_QPA_PLATFORM', 'offscreen')
from qgis.core import *
from qgis.PyQt.QtCore import QVariant, Qt, QPointF
from qgis.PyQt.QtGui import QColor, QFont, QPolygonF

OUT = Path(__file__).resolve().parent
DATA = OUT / 'data'
DATA.mkdir(exist_ok=True)
COLORS = {1: '#1469ad', 2: '#e57c19', 3: '#258b55',
          4: '#8653a5', 5: '#d3485b', 6: '#07878d'}
STYLES = {1: 'solid', 2: 'solid', 3: 'dash', 4: 'dash', 5: 'dash dot', 6: 'dash dot'}
STATUS = {1: 'Operating', 2: 'Operating', 3: 'Construction / commissioning',
          4: 'Under construction', 5: 'Planned / pre-construction', 6: 'Planned / under review'}
WKT = ('LOCAL_CS["Dar BRT schematic grid (not geographic)",'
       'LOCAL_DATUM["Diagram origin",0],UNIT["diagram unit",1],'
       'AXIS["X",EAST],AXIS["Y",NORTH]]')

# name: x, y, displayed label, label dx, label dy, horizontal alignment
NODES = {
 'Kibaha': (-8, 10, 'Kibaha*', 0, 1.1, 'Center'),
 'Kibamba': (-3, 10, 'Kibamba', 0, 1.1, 'Center'),
 'Kimara': (2, 10, 'Kimara', 0, 1.1, 'Center'),
 'Ubungo': (7, 10, 'Ubungo', -.9, -1.1, 'Right'),
 'Magomeni': (13, 10, 'Magomeni', -.9, 1.45, 'Right'),
 'Fire': (18, 8, 'Fire', -.9, -.9, 'Right'),
 'Kivukoni': (25, 8, 'Kivukoni', .9, 0, 'Left'),
 'Morocco': (15, 15, 'Morocco', -.8, -.9, 'Right'),
 'Mwenge': (10, 20, 'Mwenge', -.9, -.5, 'Right'),
 'Lugalo': (10, 24, 'Lugalo', -.9, .3, 'Right'),
 'Basihaya': (5, 29, 'Tegeta /\nBoko Basihaya', -.8, 1.2, 'Right'),
 'Maktaba': (22, 12, 'CBD / Maktaba', 1, .1, 'Left'),
 'CityJunction': (20, 8, 'City junction', 3.5, 1.6, 'Left'),
 'Sokoine': (23, 6, 'CBD / Sokoine', 1.1, -.4, 'Left'),
 'Gerezani': (18, 4, 'Gerezani', .9, -1.7, 'Left'),
 'Buguruni': (12, 4, 'Buguruni', -.4, -1.1, 'Right'),
 'Tazara': (12, 0, 'TAZARA', -.9, -.6, 'Right'),
 'Airport': (7, -5, 'Airport corridor', .9, -.3, 'Left'),
 'Gongo': (2, -10, 'Gongo la Mboto', -.9, -.5, 'Right'),
 'Dampo': (7, 4, 'Tabata Dampo', -1, 0, 'Right'),
 'Segerea': (1, -2, 'Segerea', -.9, -.3, 'Right'),
 'Kigogo': (11, 8, 'Kigogo', 0, 1.2, 'Center'),
 'Veterinary': (14, -2, 'Veterinary', -.3, -1.15, 'Right'),
 'Bridge': (22, -6, 'Nyerere Bridge\napproach', 1, -.2, 'Left'),
 'Jitegemee': (21, 0, 'Jitegemee', .9, .2, 'Left'),
 'KwaAzizi': (18, -8, 'Kwa Azizi Ali /\nMbagala branch', 1.05, -.2, 'Left'),
 'Mbagala': (18, -12, 'Mbagala\nRangi Tatu', -1, -.2, 'Right'),
 'Vikindu': (23, -17, 'Vikindu area', 1, 0, 'Left'),
 'Bendera': (24, 3, 'Bendera Tatu', 1, .2, 'Left'),
 'Kawe': (15, 24, 'Kawe', 0, 1.1, 'Center'),
}

# A string references a hub; a coordinate pair is a bend with no stop symbol.
# Every source segment is retained. Added intermediate hubs are schematic
# corridor references, not assertions about official passenger transfers.
ROUTES = {
 'P1-A': ['Kimara', 'Ubungo', 'Magomeni'],
 'P1-B': ['Magomeni', (16, 10), 'Fire', 'CityJunction', 'Kivukoni'],
 'P1-C': ['Magomeni', (15, 12), 'Morocco'],
 'P1-D': ['Fire', 'Gerezani'],
 'P2-A': ['Sokoine', (23, 2), 'Jitegemee', (21, -5), 'KwaAzizi', 'Mbagala'],
 'P2-B': ['Magomeni', (13, 6), (15, 4), (15, 2), (17, 0), 'Jitegemee'],
 'P2-C': ['Gerezani', (21, 4), (22, 3), 'Bendera'],
 'P3-A': ['Maktaba', (22, 10), 'CityJunction', (20, 6), (16, 2), (14, 2), 'Tazara'],
 'P3-B': ['Tazara', 'Airport', 'Gongo'],
 'P3-C': ['Gerezani', 'Buguruni', 'Tazara'],
 'P4-A': ['Maktaba', (20, 14), (16, 14), 'Morocco'],
 'P4-B': ['Morocco', 'Mwenge', 'Lugalo', 'Basihaya'],
 'P4-C': ['Mwenge', (7, 17), 'Ubungo'],
 'P5-A': ['Ubungo', 'Dampo', 'Buguruni', 'Tazara', 'Veterinary', (18, -6), 'Bridge'],
 'P5-B': ['Dampo', (5, 2), (5, -2), 'Segerea'],
 'P5-C': ['Dampo', (7, 5), (10, 8), 'Kigogo'],
 'P5-D': ['Veterinary', (14, -4), 'KwaAzizi'],
 'P6-A': ['Morocco', (18, 18), (18, 21), 'Kawe', 'Lugalo'],
 'P6-B': ['Kimara', 'Kibamba'],
 'P6-C': ['Kibamba', 'Kibaha'],
 'P6-D': ['Mbagala', (18, -14), (21, -17), 'Vikindu'],
}

def xy(item):
    return NODES[item][:2] if isinstance(item, str) else item

def make_layer(geometry, name, fields, crs):
    layer = QgsVectorLayer(geometry, name, 'memory')
    layer.setCrs(crs)
    layer.dataProvider().addAttributes([QgsField(n, t) for n, t in fields])
    layer.updateFields()
    return layer

def write_layer(layer, name, gpkg, project):
    options = QgsVectorFileWriter.SaveVectorOptions()
    options.driverName = 'GPKG'
    options.layerName = name
    options.actionOnExistingFile = (QgsVectorFileWriter.CreateOrOverwriteLayer
                                   if gpkg.exists() else QgsVectorFileWriter.CreateOrOverwriteFile)
    result = QgsVectorFileWriter.writeAsVectorFormatV3(layer, str(gpkg), project.transformContext(), options)
    assert result[0] == QgsVectorFileWriter.NoError, result
    result_layer = QgsVectorLayer(str(gpkg) + '|layername=' + name, layer.name(), 'ogr')
    assert result_layer.isValid(), name
    return result_layer

def fixed_labels(layer, field, size, color, bold=False, buffer=True):
    settings = QgsPalLayerSettings()
    settings.fieldName = field
    settings.placement = QgsPalLayerSettings.OverPoint
    settings.displayAll = True
    properties = settings.dataDefinedProperties()
    properties.setProperty(QgsPalLayerSettings.PositionX, QgsProperty.fromExpression('$x + "label_dx"'))
    properties.setProperty(QgsPalLayerSettings.PositionY, QgsProperty.fromExpression('$y + "label_dy"'))
    for prop, source_field in [(QgsPalLayerSettings.Hali, 'halign'),
                               (QgsPalLayerSettings.Vali, 'valign')]:
        properties.setProperty(prop, QgsProperty.fromField(source_field))
    properties.setProperty(QgsPalLayerSettings.AlwaysShow, QgsProperty.fromValue(True))
    settings.setDataDefinedProperties(properties)
    fmt = QgsTextFormat()
    font = QFont('DejaVu Sans'); font.setBold(bold)
    fmt.setFont(font); fmt.setSize(size); fmt.setColor(QColor(color))
    buf = QgsTextBufferSettings(); buf.setEnabled(buffer); buf.setSize(.65); buf.setColor(QColor('white'))
    fmt.setBuffer(buf); settings.setFormat(fmt)
    layer.setLabeling(QgsVectorLayerSimpleLabeling(settings)); layer.setLabelsEnabled(True)

def build():
    app = QgsApplication.instance()
    owns_app = app is None
    if owns_app:
        app = QgsApplication([], False); app.initQgis()
    project = QgsProject()
    crs = QgsCoordinateReferenceSystem(); assert crs.createFromWkt(WKT)
    project.setCrs(crs)
    project.setEllipsoid('NONE')
    project.setFilePathStorage(Qgis.FilePathType.Relative)
    project.setBackgroundColor(QColor('white'))
    project.setTitle('Dar es Salaam BRT | subway-style schematic | 09 October 2026')
    gpkg = DATA / 'Dar_BRT_Subway.gpkg'
    if gpkg.exists(): gpkg.unlink()
    source = json.loads((DATA / 'source_corridors.geojson').read_text())
    source_by_id = {f['properties']['segment_id']: f['properties'] for f in source['features']}
    assert set(source_by_id) == set(ROUTES)

    routes = make_layer('LineString', 'Schematic corridor segments', [
        ('phase', QVariant.Int), ('segment_id', QVariant.String), ('corridor', QVariant.String),
        ('status', QVariant.String), ('snapshot', QVariant.String), ('part', QVariant.Int),
        ('from_ref', QVariant.String), ('to_ref', QVariant.String), ('shared_run', QVariant.Int),
        ('option', QVariant.Int), ('source_url', QVariant.String), ('diagram_note', QVariant.String)], crs)
    phases_at_node = {n: set() for n in NODES}
    for sid, items in ROUTES.items():
        phase = int(sid[1]); props = source_by_id[sid]
        for n in items:
            if isinstance(n, str): phases_at_node[n].add(phase)
        # Split at each hub so coincident runs can be displayed in parallel.
        start = 0; part = 0
        for end in range(1, len(items)):
            if not isinstance(items[end], str): continue
            vertices = [xy(n) for n in items[start:end+1]]
            for a, b in zip(vertices, vertices[1:]):
                dx, dy = abs(a[0]-b[0]), abs(a[1]-b[1])
                assert dx == 0 or dy == 0 or abs(dx-dy) < 1e-9, (sid, a, b)
            part += 1
            shared = int({items[start], items[end]} == {'Buguruni', 'Tazara'})
            feat = QgsFeature(routes.fields())
            feat.setAttributes([phase, sid, props['corridor'], STATUS[phase], '2026-10-09', part,
                                items[start], items[end], shared, int(sid=='P6-C'), props['source_url'],
                                'Schematic local coordinates; selected corridor references; not engineering alignment or service routing'])
            feat.setGeometry(QgsGeometry.fromPolylineXY([QgsPointXY(*p) for p in vertices]))
            routes.dataProvider().addFeatures([feat]); start = end
    routes = write_layer(routes, 'schematic_corridors', gpkg, project)

    hubs = make_layer('Point', 'Selected hubs and place references', [
        ('node_id', QVariant.String), ('name', QVariant.String), ('phases', QVariant.String),
        ('shared', QVariant.Int), ('label_dx', QVariant.Double), ('label_dy', QVariant.Double),
        ('halign', QVariant.String), ('valign', QVariant.String), ('reference_note', QVariant.String)], crs)
    for n, (x, y, name, dx, dy, halign) in NODES.items():
        phases = phases_at_node[n]
        feat = QgsFeature(hubs.fields())
        feat.setAttributes([n, name, ', '.join(map(str, sorted(phases))), int(len(phases)>1),
                            dx, dy, halign, 'Half',
                            'Selected place/corridor reference; shared symbol does not confirm a passenger interchange or platform'])
        feat.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(x, y)))
        hubs.dataProvider().addFeatures([feat])
    hubs = write_layer(hubs, 'schematic_hubs', gpkg, project)
    cats = []
    for shared, size in [(0, 2.6), (1, 4.3)]:
        symbol = QgsMarkerSymbol.createSimple({'name':'circle','color':'white','outline_color':'#26333b',
                                               'outline_width':'.55','size':str(size)})
        cats.append(QgsRendererCategory(shared, symbol, 'Shared corridor hub reference' if shared else 'Selected place / endpoint'))
    hubs.setRenderer(QgsCategorizedSymbolRenderer('shared', cats))
    fixed_labels(hubs, 'name', 9.3, '#23323d', bold=True)

    badge_positions = {1:(3.2,7.5),2:(21,-10),3:(3,-7.5),4:(7.3,29),5:(1,.1),6:(-3,7.5)}
    badges = make_layer('Point', 'Phase number badges', [
        ('phase', QVariant.Int), ('label_dx', QVariant.Double), ('label_dy', QVariant.Double),
        ('halign', QVariant.String), ('valign', QVariant.String)], crs)
    for p, (x,y) in badge_positions.items():
        feat=QgsFeature(badges.fields());feat.setAttributes([p,0,0,'Center','Half'])
        feat.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(x,y)));badges.dataProvider().addFeatures([feat])
    badges=write_layer(badges,'phase_badges',gpkg,project)
    badges.setRenderer(QgsCategorizedSymbolRenderer('phase',[
        QgsRendererCategory(p,QgsMarkerSymbol.createSimple({'name':'circle','color':color,
            'outline_style':'no','size':'5.8'}),f'Phase {p}') for p,color in COLORS.items()]))
    fixed_labels(badges,'phase',10,'white',bold=True,buffer=False)

    root=project.layerTreeRoot()
    annotations=root.addGroup('Hubs, labels and phase badges')
    current=root.addGroup('CURRENT | operating')
    construction=root.addGroup('CURRENT | construction / commissioning')
    future=root.addGroup('FUTURE | planned corridors')
    ref=root.addGroup('Data and source notes')
    def add(layer,group): project.addMapLayer(layer,False);group.addLayer(layer)
    add(hubs,annotations);add(badges,annotations)
    phase_layers=[]
    for p in range(1,7):
        layer=QgsVectorLayer(str(gpkg)+'|layername=schematic_corridors',f'Phase {p} | {STATUS[p]}','ogr')
        layer.setSubsetString(f'"phase"={p} AND "option"=0')
        renderer=QgsRuleBasedRenderer(QgsLineSymbol())
        base=renderer.rootRule();base.removeChildAt(0)
        for shared in [0,1]:
            sym=QgsLineSymbol.createSimple({'line_color':COLORS[p],'line_width':'1.5',
                 'line_style':STYLES[p],'capstyle':'round','joinstyle':'round',
                 'offset':str(.95 if shared and p==3 else -.95 if shared and p==5 else 0)})
            # White casing separates crossings, while shared runs are parallel.
            halo=QgsSimpleLineSymbolLayer.create({'line_color':'white','line_width':'2.05',
                'capstyle':'round','joinstyle':'round','offset':str(.95 if shared and p==3 else -.95 if shared and p==5 else 0)})
            sym.insertSymbolLayer(0,halo)
            rule=QgsRuleBasedRenderer.Rule(sym);rule.setFilterExpression(f'"shared_run"={shared}')
            rule.setLabel('Parallel shared corridor' if shared else 'Schematic corridor');base.appendChild(rule)
        layer.setRenderer(renderer)
        layer.setAbstract('Local schematic coordinates. Not to scale, not a service map. Selected hubs are references only. Status snapshot 09 October 2026.')
        add(layer,current if p<3 else construction if p<5 else future)
        layer.saveNamedStyle(str(DATA/f'subway_phase_{p}.qml'));phase_layers.append(layer)
    option=QgsVectorLayer(str(gpkg)+'|layername=schematic_corridors','Phase 6 | Kibaha longer option','ogr')
    option.setSubsetString('"option"=1')
    option.renderer().setSymbol(QgsLineSymbol.createSimple({'line_color':'#68abb0','line_width':'1.1',
                                                         'line_style':'dot','capstyle':'round'}))
    add(option,future)
    add(routes,ref);ref.findLayer(routes.id()).setItemVisibilityChecked(False);ref.setExpanded(False)
    render_layers=[hubs,badges]+phase_layers+[option]
    root.setHasCustomLayerOrder(True);root.setCustomLayerOrder(render_layers+[routes])
    extent=QgsRectangle(-13,-21,32,34)
    project.viewSettings().setDefaultViewExtent(QgsReferencedRectangle(extent,crs))
    bm=QgsBookmark();bm.setName('Entire subway schematic');bm.setExtent(QgsReferencedRectangle(extent,crs));project.bookmarkManager().addBookmark(bm)
    project.setCustomVariables({'diagram_type':'Subway-style schematic','status_snapshot':'2026-10-09',
                                'coordinate_warning':'Local diagram grid; not geographical coordinates'})

    layout=QgsPrintLayout(project);layout.initializeDefaults();layout.setName('Dar BRT | Subway schematic')
    layout.pageCollection().pages()[0].setPageSize('A3',QgsLayoutItemPage.Portrait)
    def text(txt,x,y,w,h,size=10,color='#23323d',bold=False):
        label=QgsLayoutItemLabel(layout);label.setText(txt)
        font=QFont('DejaVu Sans');font.setPointSizeF(size);font.setBold(bold);label.setFont(font);label.setFontColor(QColor(color))
        layout.addLayoutItem(label);label.attemptMove(QgsLayoutPoint(x,y));label.attemptResize(QgsLayoutSize(w,h));return label
    text('DAR ES SALAAM',12,9,215,13,24,bold=True)
    text('BRT NETWORK',12,23,200,11,16,color='#5b6d79')
    text('SUBWAY-STYLE SCHEMATIC',12,36,210,8,9,color='#5b6d79',bold=True)
    text('CURRENT + FUTURE\n09 OCTOBER 2026',224,13,62,21,9,color='#5b6d79')
    def stroke(x1,y1,x2,y2,color,width=.25,style='solid'):
        line=QgsLayoutItemPolyline(QPolygonF([QPointF(x1,y1),QPointF(x2,y2)]),layout)
        line.setSymbol(QgsLineSymbol.createSimple({'line_color':color,'line_width':str(width),'line_style':style,'capstyle':'round'}));layout.addLayoutItem(line)
    stroke(12,47,285,47,'#cbd5dc')
    item=QgsLayoutItemMap(layout);layout.addLayoutItem(item)
    item.attemptMove(QgsLayoutPoint(8,49));item.attemptResize(QgsLayoutSize(281,292))
    item.setCrs(crs);item.setLayers(render_layers);item.setKeepLayerSet(True);item.zoomToExtent(extent)
    stroke(12,344,285,344,'#cbd5dc')
    subtitles={1:'Kimara · Morocco · CBD',2:'Kilwa · Mbagala · Kawawa South',
               3:'Airport corridor · Gongo la Mboto',4:'Tegeta · Mwenge · Ubungo',
               5:'Mandela · Tabata · Kigogo',6:'Kawe · western / southern extensions'}
    for p in range(1,7):
        col=(p-1)%3;row=(p-1)//3;x=12+col*93;y=350+row*20
        stroke(x,y+3,x+13,y+3,COLORS[p],1.6,STYLES[p])
        text(f'{p}  PHASE {p}',x+17,y-1,73,7,9,bold=True)
        text('Operating' if p<3 else 'Construction' if p<5 else 'Planned',x+17,y+5,73,6,8,color='#5b6d79')
        text(subtitles[p],x,y+12,91,6,7.2,color='#5b6d79')
    text('Circles mark selected places. Large circles mark shared corridor references.\nNo symbol confirms an operational passenger interchange. This is not a complete station map.',12,389,273,10,7.4,color='#5b6d79')
    text('SCHEMATIC · NOT TO SCALE',12,399,135,7,9,bold=True)
    text('* Kibaha is the longer Phase 6 option; the western terminus is subject to review.\nPhase 7: planning note only. Sources: DART / TANROADS / dated reporting. See README and sources.csv.',12,408,273,10,7,color='#5b6d79')
    project.layoutManager().addLayout(layout)
    project.setFileName(str(OUT/'Dar_BRT_Subway_Schematic.qgz'));assert project.write()
    export=QgsLayoutExporter.ImageExportSettings();export.dpi=160
    assert QgsLayoutExporter(layout).exportToImage(str(OUT/'Dar_BRT_Subway_Preview.png'),export)==QgsLayoutExporter.Success
    print(json.dumps({'layers':len(project.mapLayers()),'source_segments':len(ROUTES),
                      'diagram_parts':routes.featureCount(),'selected_hubs':hubs.featureCount(),
                      'crs':project.crs().description(),'project':project.fileName()}),flush=True)
    # Reopen verification is done in a separate process; this also works while
    # rebuilding from inside QGIS, where layers may still hold provider handles.

if __name__ == '__main__':
    standalone_app = None
    if QgsApplication.instance() is None:
        standalone_app = QgsApplication([], False)
        standalone_app.initQgis()
    build()
    if standalone_app is not None:
        standalone_app.exitQgis()
