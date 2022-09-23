// This will let you use the .remove() function later on
if (!("remove" in Element.prototype)) {
  Element.prototype.remove = function () {
    if (this.parentNode) {
      this.parentNode.removeChild(this);
    }
  };
}

mapboxgl.accessToken = document.getElementById("mapboxToken").value;

// Set bounds to Uganda
var uganda = [
  [29.57, -1.48],
  [35.0, 4.23],
];
// This adds the map to your page
var map = new mapboxgl.Map({
  container: "map",
  style: "mapbox://styles/kollinsayz/cl8dlah1e001214msulqh1czl/?fresh=true",
  center: [32.365, 1.302],
  //center: shimoni,
  zoom: 6.39,
  maxZoom: 10,
  minZoom: 6,
  attributionControl: false,
});

// Disable default box zooming.
map.boxZoom.disable();
map.scrollZoom.disable();

let hoveredDistrictId = null;
let clickedDistrictId = null;

map.on("load", function () {
  // add generic districts
  map.addSource("districts", {
    type: "geojson",
    data: districts_geojson,
  });
  // lazy load project districts
  map.addSource("project_districts", {
    type: "geojson",
    data: project_districts,
  });
  // add coordinating centres

  // map.addSource('centres', {
  //     type: 'geojson',
  //     data: centres,
  //     cluster: true,
  //     clusterRadius: 50 // Radius of each cluster when clustering points (defaults to 50)
  // });

  // add Core PTCs
  // map.addSource('colleges', {
  //     type: 'geojson',
  //     data: colleges
  // });
  // Hub distance

  // map.addSource('distances', {
  //     type: 'geojson',
  //     data: distances
  // });

  // distance layers with idle, hover and mouseover functions
  // The feature-state dependent fill-opacity expression will render the hover effect
  // when a feature's hover state is set to true.
  map.addLayer({
    id: "district-fills",
    type: "fill",
    source: "project_districts",
    layout: {},
    paint: {
      "fill-color": "#346CB0",
      "fill-opacity": [
        "case",
        ["boolean", ["feature-state", "hover"], false],
        1,
        0.6,
      ],
    },
  });

  map.addLayer({
    id: "district-borders",
    type: "line",
    source: "districts",
    layout: {},
    paint: {
      "line-color": "#346CB0",
      "line-width": 1,
    },
  });

  map.addLayer({
    id: "district-fills-click",
    type: "fill",
    source: "project_districts",
    layout: {},
    paint: {
      "fill-color": "#346CB0",
      "fill-opacity": [
        "case",
        ["boolean", ["feature-state", "click"], false],
        1,
        0,
      ],
    },
  });

  // When the user moves their mouse over the state-fill layer, we'll update the
  // feature state for the feature under the mouse.
  map.on("mousemove", "district-fills", (e) => {
    if (e.features.length > 0) {
      if (hoveredDistrictId !== null) {
        map.setFeatureState(
          {
            source: "project_districts",
            id: hoveredDistrictId,
          },
          {
            hover: false,
          }
        );
      }
      hoveredDistrictId = e.features[0].id;
      map.setFeatureState(
        {
          source: "project_districts",
          id: hoveredDistrictId,
        },
        {
          hover: true,
        }
      );
    }
  });

  map.on("mouseenter", "district-fills", () => {
    map.getCanvas().style.cursor = "pointer";
  });

  // When the mouse leaves the state-fill layer, update the feature state of the
  // previously hovered feature.
  map.on("mouseleave", "district-fills", () => {
    if (hoveredDistrictId !== null) {
      map.setFeatureState(
        {
          source: "project_districts",
          id: hoveredDistrictId,
        },
        {
          hover: false,
        }
      );
    }
    hoveredDistrictId = null;
    // change cursor back to normal when leave districts
    map.getCanvas().style.cursor = "";
  });

  // map.addLayer({
  //     'id': 'centres-layer',
  //     'type': 'circle',
  //     'source': 'centres',
  //     filter: ['has', 'point_count'],
  //     paint: {
  //         // Use step expressions (https://docs.mapbox.com/mapbox-gl-js/style-spec/#expressions-step)
  //         // with three steps to implement three types of circles:
  //         //   * Blue, 20px circles when point count is less than 100
  //         //   * Yellow, 30px circles when point count is between 100 and 750
  //         //   * Pink, 40px circles when point count is greater than or equal to 750
  //         'circle-color': [
  //             'step',
  //             ['get', 'point_count'],
  //             '#51bbd6',
  //             100,
  //             '#f1f075',
  //             750,
  //             '#f28cb1'
  //         ],
  //         'circle-radius': [
  //             'step',
  //             ['get', 'point_count'],
  //             20,
  //             100,
  //             30,
  //             750,
  //             40
  //         ]
  //     }
  // });
  // map.addLayer({
  //     id: 'cluster-count',
  //     type: 'symbol',
  //     source: 'centres',
  //     filter: ['has', 'point_count'],
  //     layout: {
  //         'text-field': '{point_count_abbreviated}',
  //         'text-font': ['DIN Offc Pro Medium', 'Arial Unicode MS Bold'],
  //         'text-size': 12
  //     }
  // });

  // map.addLayer({
  //     id: 'unclustered-point',
  //     type: 'circle',
  //     source: 'centres',
  //     filter: ['!', ['has', 'point_count']],
  //     paint: {
  //         'circle-color': '#11b4da',
  //         'circle-radius': 4,
  //         'circle-stroke-width': 1,
  //         'circle-stroke-color': '#fff'
  //     }
  // });

  // map.addLayer({
  //     'id': 'colleges-layer',
  //     'type': 'circle',
  //     'source': 'colleges',
  //     'paint': {
  //         'circle-radius': 8,
  //         'circle-stroke-width': 2,
  //         'circle-color': 'red',
  //         'circle-stroke-color': 'white'
  //     }
  // });

  // Add hub distance layer
  // map.addLayer({
  //     'id': 'distances-layer',
  //     'type': 'line',
  //     'source': 'distances',
  //     'paint': {
  //         'line-color': '#69347c',
  //         'line-width': 1
  //     }
  // });

  map.resize();
});

// After the last frame rendered before the map enters an "idle" state.
map.on("idle", () => {
  // If these two layers were not added to the map, abort
  if (!map.getLayer("colleges-layer") || !map.getLayer("centres-layer")) {
    return;
  }

  // Enumerate ids of the layers.
  const toggleableLayerIds = [
    "colleges-layer",
    "centres-layer",
    "distances-layer",
  ];

  // Set up the corresponding toggle button for each layer.
  for (const id of toggleableLayerIds) {
    // Skip layers that already have a button set up.
    if (document.getElementById(id)) {
      continue;
    }

    // Create a link.
    const link = document.createElement("a");
    link.id = id;
    link.href = "#";
    link.textContent = id;
    link.className = "active";

    // Show or hide layer when the toggle is clicked.
    link.onclick = function (e) {
      const clickedLayer = this.textContent;
      e.preventDefault();
      e.stopPropagation();

      const visibility = map.getLayoutProperty(clickedLayer, "visibility");

      // Toggle layer visibility by changing the layout object's visibility property.
      if (visibility === "visible") {
        map.setLayoutProperty(clickedLayer, "visibility", "none");
        this.className = "";
      } else {
        this.className = "active";
        map.setLayoutProperty(clickedLayer, "visibility", "visible");
      }
    };

    const layers = document.getElementById("menu");
    layers.appendChild(link);
  }
});

map.on("click", "district-fills-click", function (e) {
  if (e.features.length > 0) {
    if (clickedDistrictId) {
      map.setFeatureState(
        {
          source: "districts",
          id: clickedDistrictId,
        },
        {
          click: false,
        }
      );
    }
    clickedDistrictId = e.features[0].id;
    map.setFeatureState(
      {
        source: "districts",
        id: clickedDistrictId,
      },
      {
        click: true,
      }
    );
  }

  var bbox = turf.bbox(e.features[0]);

  bbox[0] = bbox[0] - 1;
  bbox[2] = bbox[2] + 2.7;

  map.fitBounds(bbox, {
    padding: 200,
  });

  district_feat = e.features[0];
  var district_name = document.getElementById("districtModalDrawerLabel");
  district_name.innerHTML = district_feat.properties.name;
  var district_data = document.getElementById("districtContent");
  district_data.innerHTML =
    "<h1>" + district_feat.properties.population + "</h1>";

  // show drawer modal when district is clicked
  $("#districtModalDrawer").modal("show");
});
