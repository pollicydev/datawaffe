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
  // // lazy load project districts
  // map.addSource("project_districts", {
  //   type: "geojson",
  //   data: project_districts,
  // });

  map.addLayer({
    id: "district-fills",
    type: "fill",
    source: "districts",
    layout: {},
    paint: {
      "fill-color": "#EDF6FD",
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
      "line-color": "#999999",
      "line-width": 1,
    },
  });

  map.addLayer({
    id: "district-fills-click",
    type: "fill",
    source: "districts",
    layout: {},
    paint: {
      "fill-color": "#0D5BDD",
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
            source: "districts",
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
          source: "districts",
          id: hoveredDistrictId,
        },
        {
          hover: true,
        }
      );
    }
  });

  // Create a popup, but don't add it to the map yet.
  const popup = new mapboxgl.Popup({
    closeButton: false,
    closeOnClick: false,
  });

  map.on("mousemove", "district-fills", (e) => {
    map.getCanvas().style.cursor = "pointer";

    const name = e.features[0].properties.name;

    // Populate the popup and set its coordinates
    // based on the feature found.
    popup
      .setLngLat(e.lngLat)
      .setHTML("<h5>" + name + "</h5><p>Click for details</p>")
      .addTo(map);
  });

  // When the mouse leaves the state-fill layer, update the feature state of the
  // previously hovered feature.
  map.on("mouseleave", "district-fills", () => {
    if (hoveredDistrictId !== null) {
      map.setFeatureState(
        {
          source: "districts",
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
    popup.remove();
  });

  map.resize();
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
});
