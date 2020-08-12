var map, osm;
var vector, sLayer, areaLayer, valuesLayer, contoursLayer, contoursLayer2, contoursLayer3, contoursLayer4;
var gphy, gmap, ghyb, gsat;
var controls, barControls, graticuleCtl1, pdfLayer;
var mainbar, subBar;
var areaChanged = false;
var datesChanged = false;

//set up projections
// World Geodetic System 1984 projection
var EPSG4326 = ol.proj.get('EPSG:4326');
var EPSG3857 = ol.proj.get('EPSG:3857');
// WGS84 Google Mercator projection
var GOOGLE_MERCATOR = ol.proj.get('EPSG:900913');

// Define three colors that will be used to style the cluster features
// depending on the number of features they contain.
var colors = {
    low: "rgb(181, 226, 140)",
    middle: "rgb(241, 211, 87)",
    high: "rgb(253, 156, 115)"
};

// Create layers instances
var layerOSM = new ol.layer.Tile({
    title: 'Open Street Map',
    source: new ol.source.OSM(),
    type: 'base'
});

// Current search area selection
sLayer = new ol.layer.Vector({
    title: 'Search area polygon',
    source: new ol.source.Vector({
        type: 'data'
    }),
    style: new ol.style.Style({
        image: new ol.style.Circle({
            radius: 5,
            stroke: new ol.style.Stroke({
                color: 'rgb(255,165,0)',
                width: 3
            }),
            fill: new ol.style.Fill({
                color: 'rgba(255,165,0,.3)'
            })
        }),
        stroke: new ol.style.Stroke({
            color: 'rgb(255,165,0)',
            width: 3
        }),
        fill: new ol.style.Fill({
            color: 'rgba(255,165,0,.3)'
        })
    })
});

var dataurl = '../data.geojson';
areaLayer = new ol.layer.Vector({
    title: 'Area',
    source: new ol.source.Vector({
        format: new ol.format.GeoJSON(),
        url: dataurl,
        type: 'data'
    })
});

//  Vector layer
vector = new ol.layer.Vector({
    title: 'User vector',
    source: new ol.source.Vector({
        type: 'data'
    })
});

/* Nested subbars */
subBar = new ol.control.Bar({
    toggleOne: true,
    controls: [
        new ol.control.Button({
            html: '<i class="fa fa-info"></i>',
            title: "Show informations",
            handleClick: function () {
                switch (selectCtrl.getInteraction().getFeatures().getLength()) {
                    case 0:
                        console.log("Select an object first...");
                        break;
                    case 1:
                        var f = selectCtrl.getInteraction().getFeatures().item(0);
                        console.log("Selection is a " + f.getGeometry().getType());
                        break;
                    default:
                        console.log(selectCtrl.getInteraction().getFeatures().getLength() + " objects seleted.");
                        break;
                }
            }
        }),
        new ol.control.Button({
            html: '<i class="fa fa-times"></i>',
            title: "Delete",
            handleClick: function () {
                var features = selectCtrl.getInteraction().getFeatures();
                if (!features.getLength()) console.log("Select an object first...");
                else console.log(features.getLength() + " object(s) deleted.");
                for (var i = 0, f; f = features.item(i); i++) {
                    vector.getSource().removeFeature(f);
                }
                selectCtrl.getInteraction().getFeatures().clear();
            }
        })
    ]
});

// Add editing tools
var selectCtrl = new ol.control.Toggle({
    html: '<i class="fa fa-hand-pointer"></i>',
    title: "Select",
    interaction: new ol.interaction.Select(),
    bar: subBar,
    autoActivate: true,
    active: true
});

var pedit = new ol.control.Toggle({
    html: '<i class="fa fa-map-marker-alt" ></i>',
    title: 'Point',
    interaction: new ol.interaction.Draw
    ({
        type: 'Point',
        source: vector.getSource()
    })
});

var ledit = new ol.control.Toggle({
    html: '<i class="fa fa-share-alt" ></i>',
    title: 'LineString',
    interaction: new ol.interaction.Draw
    ({
        type: 'LineString',
        source: vector.getSource(),
        // Count inserted points
        geometryFunction: function (coordinates, geometry) {
            if (geometry) geometry.setCoordinates(coordinates);
            else geometry = new ol.geom.LineString(coordinates);
            this.nbpts = geometry.getCoordinates().length;
            return geometry;
        }
    }),
    // Options bar associated with the control
    bar: new ol.control.Bar({
        controls: [
            new ol.control.Button({
                html: '<i class="fas fa-undo-alt"></i>',
                title: "Delete last point",
                handleClick: function () {
                    if (ledit.getInteraction().nbpts > 1) ledit.getInteraction().removeLastPoint();
                }
            }),
            new ol.control.Button({
                html: '<i class="fas fa-stop"></i>',
                title: "Finish",
                handleClick: function () {	// Prevent null objects on finishDrawing
                    if (ledit.getInteraction().nbpts > 2) ledit.getInteraction().finishDrawing();
                }
            })
        ]
    })
});


var fedit = new ol.control.Toggle({
    html: '<i class="far fa-bookmark fa-rotate-270"></i>',
    title: 'Polygon',
    interaction: new ol.interaction.Draw({
        type: 'Polygon',
        source: vector.getSource(),
        // Count inserted points
        geometryFunction: function (coordinates, geometry) {
            this.nbpts = coordinates[0].length;
            if (geometry) geometry.setCoordinates([coordinates[0].concat([coordinates[0][0]])]);
            else geometry = new ol.geom.Polygon(coordinates);
            return geometry;
        }
    }),
    // Options bar ssociated with the control
    bar: new ol.control.Bar({
        controls: [
            new ol.control.Button({
                html: '<i class="fas fa-undo-alt"></i>',
                title: "Undo last point",
                handleClick: function () {
                    if (fedit.getInteraction().nbpts > 1) fedit.getInteraction().removeLastPoint();
                }
            }),
            new ol.control.Button({
                html: '<i class="fas fa-stop"></i>',
                title: "Finish",
                handleClick: function () {	// Prevent null objects on finishDrawing
                    if (fedit.getInteraction().nbpts > 3) fedit.getInteraction().finishDrawing();
                }
            })
        ]
    })
});

// Add a simple push button to save features
var save = new ol.control.Button({
    html: '<i class="fa fa-download"></i>',
    title: "Save",
    handleClick: function (e) {
        var json = new ol.format.GeoJSON().writeFeatures(vector.getSource().getFeatures());
        console.log(json);
    }
});

// Create toolbar controls
barControls = [
    new ol.control.Attribution(),
    new ol.control.ZoomToExtent({extent: [350000, 4000000, 370000, 8000000]}),
    new ol.control.Rotate(),
    new ol.control.FullScreen(),
    new ol.control.Toggle({
        html: '<i class="fas fa-map-marked-alt"></i>',
        title: "Open edit subbar",
        // First level nested control bar
        bar: new ol.control.Bar({
            toggleOne: true,
            controls: [
                selectCtrl,
                pedit,
                ledit,
                fedit,
                save
            ]
        }),
        onToggle: function () {
            console.log("Edit subbar pressed");
        },
    }),
    new ol.control.OverviewMap({
        collapsed: true
    })
];

mainbar = new ol.control.Bar({
    controls: barControls
});

// Create controls
controls = [
    new ol.control.MousePosition({
        undefinedHTML: 'outside',
        projection: EPSG4326,
        coordinateFormat: function (coordinate) {
            return ol.coordinate.format(coordinate, '{x}, {y}', 4);
        }
    }),
    new ol.control.LayerSwitcher({
        tipLabel: 'Legend' // Optional label for button
    }),
    new ol.control.ScaleLine(),
    new ol.control.Zoom()
];


// Set the search control
var search = new ol.control.SearchNominatim({
    //target: $(".options").get(0),
    polygon: $('#polygon').prop('checked'),
    position: true	// Search, with priority to geo position
});


var corineUrl = 'http://filotis.itia.ntua.gr/mapserver?SERVICE=WFS&' +
    'VERSION=1.1.0&REQUEST=GetFeature&TYPENAME=biotopes_corine&' +
    'SRSNAME=EPSG:4326&OUTPUTFORMAT=gml3';
var naturaUrl = 'http://filotis.itia.ntua.gr/mapserver?SERVICE=WFS&' +
    'VERSION=1.1.0&REQUEST=GetFeature&TYPENAME=biotopes_natura&' +
    'SRSNAME=EPSG:4326&OUTPUTFORMAT=gml3';
var cadastreUrl = 'http://gis.ktimanet.gr/wms/wmsopen/wmsserver.aspx';


function applyMargins() {
    var leftToggler = $(".mini-submenu-left");
    var rightToggler = $(".mini-submenu-right");
    var sideBarWidth = $(".sidebar-left").width();
    if (leftToggler.is(":visible")) {
        $("#map .ol-zoom")
            .css("margin-left", 0)
            .removeClass("zoom-top-opened-sidebar")
            .addClass("zoom-top-collapsed");
        $("#map .nominatim")
            .css("margin-left", 0)
            .removeClass("search-top-opened-sidebar")
            .addClass("search-top-collapsed");
    } else {
        $("#map .ol-zoom")
            .css("margin-left", sideBarWidth + 10)
            .removeClass("zoom-top-opened-sidebar")
            .removeClass("zoom-top-collapsed");
        $("#map .nominatim")
            .css("margin-left", sideBarWidth + 10)
            .removeClass("search-top-opened-sidebar")
            .removeClass("search-top-collapsed");
    }
    if (rightToggler.is(":visible")) {
        $("#map .ol-rotate")
            .css("margin-right", 0)
            .removeClass("zoom-top-opened-sidebar")
            .addClass("zoom-top-collapsed");
    } else {
        $("#map .ol-rotate")
            .css("margin-right", $(".sidebar-right").width())
            .removeClass("zoom-top-opened-sidebar")
            .removeClass("zoom-top-collapsed");
    }
}

function isConstrained() {
    return $("div.mid").width() == $(window).width();
}

function applyInitialUIState() {
    if (isConstrained()) {
        $(".sidebar-left .sidebar-body").fadeOut('slide');
        $(".sidebar-right .sidebar-body").fadeOut('slide');
        $('.mini-submenu-left').fadeIn();
        $('.mini-submenu-right').fadeIn();
    }
}

$(function () {
    $('.sidebar-left .slide-submenu').on('click', function () {
        var thisEl = $(this);
        thisEl.closest('.sidebar-body').fadeOut('slide', function () {
            $('.mini-submenu-left').fadeIn();
            applyMargins();
        });
    });

    $('.mini-submenu-left').on('click', function () {
        var thisEl = $(this);
        $('.sidebar-left .sidebar-body').toggle('slide');
        thisEl.hide();
        applyMargins();
    });

    $('.sidebar-right .slide-submenu').on('click', function () {
        var thisEl = $(this);
        thisEl.closest('.sidebar-body').fadeOut('slide', function () {
            $('.mini-submenu-right').fadeIn();
            applyMargins();
        });
    });

    $('.mini-submenu-right').on('click', function () {
        var thisEl = $(this);
        $('.sidebar-right .sidebar-body').toggle('slide');
        thisEl.hide();
        applyMargins();
    });

    $(window).on("resize", applyMargins);

    map = new ol.Map({
        target: 'map', // The DOM element that will contains the map
        renderer: 'canvas', // Force the renderer to be used
        controls: controls,
        layers: [
            new ol.layer.Group({
                title: 'Base map',
                layers: [
                    new ol.layer.Group({
                        title: 'Water color with labels',
                        type: 'base',
                        combine: true,
                        visible: false,
                        layers: [
                            new ol.layer.Tile({
                                source: new ol.source.Stamen({
                                    layer: 'watercolor'
                                })
                            }),
                            new ol.layer.Tile({
                                source: new ol.source.Stamen({
                                    layer: 'terrain-labels'
                                })
                            })
                        ]
                    }),
                    new ol.layer.Tile({
                        title: 'Water color',
                        type: 'base',
                        visible: false,
                        source: new ol.source.Stamen({
                            layer: 'watercolor'
                        })
                    }),
                    layerOSM,
                ]
            }),
            new ol.layer.Group({
                title: 'Data',
                layers: [
                    vector,
                    sLayer,
                    areaLayer,
                    new ol.layer.Vector({
                        title: 'Natura biotopes',
                        projection: ol.proj.transform([24.00, 38.00], EPSG4326, EPSG3857),
                        source: new ol.source.Vector({
                            format: new ol.format.WFS(),
                            url: naturaUrl
                        })
                    })
                ]
            })
        ],
        // Create a view centered on the specified location and zoom level
        view: new ol.View({
            center: ol.proj.transform([24.00, 38.00], EPSG4326, EPSG3857),
            zoom: 6
        }),
        interactions: ol.interaction.defaults({altShiftDragRotate: false, pinchRotate: false}),
    });

    map.addControl(search);

    // Listen for changes on chekcboxes
    $('input.mySlider:checkbox').on('change', function (event) {
        var index = $('input.mySlider:checkbox').index(event.target);
        var checked = $(event.target).is(':checked');

        if (checked) {
            map.addControl(controls[index]);
        } else {
            map.removeControl(controls[index]);
        }
    });

    map.addControl(mainbar);
    $('input.Toolbar:checkbox').on('change', function (event) {
        var checked = $(event.target).is(':checked');

        if (checked) {
            map.addControl(mainbar);
        } else {
            map.removeControl(mainbar);
        }
    });
    mainbar.setPosition('bottom');

    /* Toggle GeoJSON polygon of search area */
    $('#polygon').on('click', function () {
        search.set('polygon', $('#polygon').prop('checked'));
        search.search();
    });

    /* Select feature when click on the reference index */
    search.on('select', function (e) {
        sLayer.getSource().clear();
        // Check if we get a geojson to describe the search
        if (e.search.geojson) {
            var format = new ol.format.GeoJSON();
            var f = format.readFeature(e.search.geojson, {
                dataProjection: EPSG4326,
                featureProjection: map.getView().getProjection()
            });
            sLayer.getSource().addFeature(f);
            var view = map.getView();
            var resolution = view.getResolutionForExtent(f.getGeometry().getExtent(), map.getSize());
            var zoom = view.getZoomForResolution(resolution);
            var center = ol.extent.getCenter(f.getGeometry().getExtent());
            // redraw before zoom
            setTimeout(function () {
                view.animate({
                    center: center,
                    zoom: Math.min(zoom, 16)
                });
            }, 100);
        }
        else {
            map.getView().animate({
                center: e.coordinate,
                zoom: Math.max(map.getView().getZoom(), 16)
            });
        }
    });

    var grat =
        {
            '4326': new ol.control.Graticule({
                step: 0.1,
                stepCoord: 5,
                margin: 5,
                projection: 'EPSG:4326',
                formatCoord: function (c) {
                    return c.toFixed(1) + "°"
                }
            }),
        };

    var g;

    function setGraticule(proj) {
        if (g) map.removeControl(g);
        g = grat['4326'];
        var c = 'grey';
        var style = new ol.style.Style();
        if ($("#line").prop('checked')) style.setStroke(new ol.style.Stroke({color: c, width: 1}));
        if ($("#border").prop('checked')) style.setFill(new ol.style.Fill({color: $("#line").prop('checked') ? "#fff" : "#000"}));
        if ($("#coords").prop('checked')) style.setText(new ol.style.Text(
            {
                stroke: new ol.style.Stroke({color: "#fff", width: 2}),
                fill: new ol.style.Fill({color: c}),
            }));
        g.setStyle(style);
        map.addControl(g);
        if (proj && ol.proj.get(g.get('projection')).getExtent()) {
            var ext = ol.proj.get(g.get('projection')).getExtent();
            ext = ol.proj.transformExtent(ext, g.get('projection'), map.getView().getProjection());
            map.getView().fit(ext, ol.proj.get(g.get('projection')).getExtent(), map.getSize());
            map.getView().setZoom(map.getView().getZoom() + 1)
        }
    }

    $('input.Graticule:checkbox').on('change', function (event) {
        var checked = $(event.target).is(':checked');

        if (checked) {
            setGraticule();
        } else {
            setGraticule();
        }
    });

    setGraticule();

    applyInitialUIState();
    applyMargins();
    // console.log("DOM loaded");
})
