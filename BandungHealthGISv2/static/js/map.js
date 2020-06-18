$(document).ready(function(){
console.log("map js oke")
var Layer1 = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
{attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'});
var Layer2 = L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_nolabels/{z}/{x}/{y}{r}.png', {
attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>'});


// load GeoJSON from an external file
URLpkm = "static/data/areaPkm.geojson";
URLkec = "static/data/areaKec.geojson";
URLtpkm = "static/data/titikPkm.geojson";

/*
// load GeoJSON from an external file
URLpkm = "https://raw.githubusercontent.com/Nadiazka/Bandung-Health-GIS/master/BandungHealthGISv2/static/data/areaPkm.geojson";
URLkec = "https://raw.githubusercontent.com/Nadiazka/Bandung-Health-GIS/master/BandungHealthGISv2/static/data/areaKec.geojson";
URLtpkm = "https://raw.githubusercontent.com/Nadiazka/Bandung-Health-GIS/master/BandungHealthGISv2/static/data/titikPkm.geojson";
*/

// get Kecamatan
kec = {}
$.ajax({
    method: "GET",
    url: '/Kecamatan/',
    success: function(data){
      for (var i = 0 ; i < data.length ; i++) {
                kec[data[i].kode_kec] = {"area" : data[i].nama_kec, "kasus" :"-"};
            };
    },
    error: function(error_data){
        console.log("error")
      }
    });
console.log(kec)
//general fitur
function resetHighlight(e) {
	var layer = e.target;

	layer.setStyle({
	    weight: 2,
	    opacity: 1,
	    color: 'white',
	    dashArray: '3',
	    fillOpacity: 0.7
	});
}

function zoomToFeature(e) {
    map.fitBounds(e.target.getBounds());
  }

//Puskesmas
dataPkm = {}
dataPuskesmas = {}
$.ajax({
    method: "GET",
    url: '/Puskesmas/',
    success: function(data){
      for (var i = 0; i < data.length; i++) {
        dataPuskesmas[data[i].kode_pkm] = {"area" : data[i].nama_pkm, "kasus" :"tidak ada data "};
      };
      for (var i = 0; i < areaPkm.length; i++) {
        dataPkm[areaPkm[i].kode__kode_pkm] = {"area" : areaPkm[i].kode__kode_pkm__nama_pkm, "kasus" : areaPkm[i].kasus};
      };
      $.extend(dataPuskesmas, dataPkm)
    },
    error: function(error_data){
        console.log("error")
      }
    });

var LayerPkm = L.layerGroup();

function stylePkm(feature) {
	return {
	      fillColor: getColorPkm(dataPuskesmas[feature.properties.kode_kode].kasus),
	      weight: 2,
	      opacity: 1,
	      color: 'white',
	      dashArray: '3',
	      fillOpacity: 0.7
	  };
}

function highlightFeaturePkm(e) {
	var layer = e.target;

	layer.setStyle({
	    weight: 5,
	    color: '#666',
	    dashArray: '',
	    fillOpacity: 0.7
	});

	if (!L.Browser.ie && !L.Browser.opera && !L.Browser.edge) {
	    layer.bringToFront();
	  }

	var out = [];
	out.push("Wilayah kerja puskesmas : "+layer.feature.properties.Name);
	out.push("Jumlah kasus : "+ dataPuskesmas[layer.feature.properties.kode_kode].kasus + " kasus");
	layer.bindPopup(out.join("<br />"));
	layer.on('mouseover', function (e) {
        this.openPopup();
        });
    layer.on('mouseout', function (e) {
        this.closePopup();
    });
}

function onEachFeaturePkm(feature, layer) {
	layer.on({
	    mouseover: highlightFeaturePkm,
	    mouseout: resetHighlight,
	    click: zoomToFeature
	});
}

function getColorPkm(d) {
      return d > statPkm.kasus__max  ? '#800026' :
              d > Math.round(0.8*(statPkm.kasus__max-statPkm.kasus__min)) ? '#BD0026' :
              d > Math.round(0.6*(statPkm.kasus__max-statPkm.kasus__min))  ? '#E31A1C' :
              d > Math.round(0.4*(statPkm.kasus__max-statPkm.kasus__min))  ? '#FC4E2A' :
              d > Math.round(0.2*(statPkm.kasus__max-statPkm.kasus__min))  ? '#FD8D3C' :
              d > statPkm.kasus__min  ? '#FEB24C' :
              d >= 0  ? '#FFEDA0':
                       '#BCADA9';
  }

$.getJSON(URLpkm,function(data){
  console.log(data);
	L.geoJson(data, {
	style: stylePkm,
	onEachFeature: onEachFeaturePkm
	}).addTo(LayerPkm);
});


//Kecamatan
dataKec = {}
dataKecamatan = {}
$.ajax({
    method: "GET",
    url: '/Kecamatan/',
    success: function(data){
      console.log(data)
      for (var i = 0; i < data.length; i++) {
        dataKecamatan[data[i].kode_kec] = {"area" : data[i].nama_kec, "kasus" :"tidak ada data "};
      };
      for (var i = 0; i < areaKec.length; i++) {
        dataKec[areaKec[i].kode__kode_pkm__kode_kec] = {
          "area" : areaKec[i].kode__kode_pkm__kode_kec__nama_kec, 
          "kasus" : areaKec[i].kasus
        };
      };
      $.extend(dataKecamatan, dataKec)
    },
    error: function(error_data){
        console.log("error")
      }
    });
console.log(dataKecamatan)
console.log(dataKec)

var LayerKec = L.layerGroup();

function styleKec(feature) {
  return {
        fillColor: getColorKec(dataKecamatan[feature.properties.kode_kode].kasus),
        weight: 2,
        opacity: 1,
        color: 'white',
        dashArray: '3',
        fillOpacity: 0.7
    };
}

function highlightFeatureKec(e) {
  var layer = e.target;

  layer.setStyle({
      weight: 5,
      color: '#666',
      dashArray: '',
      fillOpacity: 0.7
  });

  if (!L.Browser.ie && !L.Browser.opera && !L.Browser.edge) {
      layer.bringToFront();
    }

  var out = [];
out.push("Kecamatan : "+layer.feature.properties.Name);
out.push("Jumlah kasus : "+ dataKecamatan[layer.feature.properties.kode_kode].kasus + " kasus");
layer.bindPopup(out.join("<br />"));
layer.on('mouseover', function (e) {
      this.openPopup();
      });
  layer.on('mouseout', function (e) {
      this.closePopup();
  });
}

function onEachFeatureKec(feature, layer) {
  layer.on({
      mouseover: highlightFeatureKec,
      mouseout: resetHighlight,
      click: zoomToFeature
  });
}

function getColorKec(d) {
      return d > statKec.kasus__max  ? '#800026' :
              d > Math.round(0.8*(statKec.kasus__max-statKec.kasus__min)) ? '#BD0026' :
              d > Math.round(0.6*(statKec.kasus__max-statKec.kasus__min))  ? '#E31A1C' :
              d > Math.round(0.4*(statKec.kasus__max-statKec.kasus__min))  ? '#FC4E2A' :
              d > Math.round(0.2*(statKec.kasus__max-statKec.kasus__min))  ? '#FD8D3C' :
              d > statKec.kasus__min  ? '#FEB24C' :
              d >= 0  ? '#FFEDA0':
                       '#BCADA9';
  }

$.getJSON(URLkec,function(data){
  L.geoJson(data, {
  style: styleKec,
  onEachFeature: onEachFeatureKec
  }).addTo(LayerKec);
});

//Titik Puskesmas
var TitikPkm = L.layerGroup();
$.getJSON(URLtpkm,function(data){
    L.geoJson(data, {
    style: styleKec,
    onEachFeature: function (feature, layer) {
                   		layer.bindPopup("Puskesmas "+feature.properties.Puskesmas);
                   		layer.on('mouseover', function (e) {
				        this.openPopup();
					        });
					    layer.on('mouseout', function (e) {
					        this.closePopup();
					    });
                   	}
    }).addTo(TitikPkm);
  });

//Clustering
  var Clustering = L.layerGroup();
  var dataClustering = ["3273030", "3273020"]
  $.getJSON(URLkec,function(data){
      console.log(data);
      for (var i = 0; i < dataClustering.length; i++) {
        L.geoJson(data, {
          filter : function (feature){
            if (feature.properties.kode_kode=== dataClustering[i]) return true
          },
          style : function(feature){
            if (feature.properties.kode_kode=== dataClustering[i]) return {color: "#ff0000"};
          }
        }).addTo(Clustering);
    }
      console.log("clustering aman")
    });


// Gathering all layer
	var map = L.map('map', {
		center: [-6.914744, 107.60981],
		zoom: 12,
		layers: [Layer1, LayerPkm]
	});

	var baseMaps = {
    "Light": Layer1,
    "Dark": Layer2
	};

	var overlayMaps = {
		"Lokasi Puskesmas" : TitikPkm,
	    "Puskesmas": LayerPkm,
	    "Kecamatan" : LayerKec,
      "Clustering" : Clustering
	};

	L.control.layers(baseMaps, overlayMaps, {position:'topleft'}).addTo(map);

	//Legenda
	  var legendPkm = L.control({position: 'bottomright'});

	      legendPkm.onAdd = function (map) {
          console.log("Legenda Pkm")
          nullGrades = "tidak ada data";
          listGrades=[-1];
          range = statPkm.kasus__max-statPkm.kasus__min;
          if ( range>=5){
            listGrades.push(statPkm.kasus__min,
                Math.round(0.2*(statPkm.kasus__max-statPkm.kasus__min)),
                Math.round(0.4*(statPkm.kasus__max-statPkm.kasus__min)),
                Math.round(0.6*(statPkm.kasus__max-statPkm.kasus__min)),
                Math.round(0.8*(statPkm.kasus__max-statPkm.kasus__min)),
                statPkm.kasus__max)
          } 
            else{
              for (var i=statPkm.kasus__min; i<statPkm.kasus__max; i++){
                listGrades.push(i)
              }
            }
          console.log(listGrades)
	          var div = L.DomUtil.create('div', 'info legend'),
	              grades = listGrades,
	              labels = [],
	              from, to;
            labels.push('<i style="background:' + getColorPkm(nullGrades) + '"></i> ' +
                    nullGrades);
            console.log(grades)
            console.log(grades.length)
	          for (var i = 0; i < grades.length; i++) {
	              from = grades[i];
	              to = grades[i + 1];

	              labels.push(
                    '<i style="background:' + getColorPkm(from+1) + '"></i> ' +
                      (from+1) + (to ? '&ndash;' + to : '+'));
	          }

	          div.innerHTML = labels.join('<br>');
	          return div;
	      };

      legendPkm.addTo(map); //Buat default

    var legendKec = L.control({position: 'bottomright'});

      legendKec.onAdd = function (map) {
          console.log("Legenda kec")
          nullGrades = "tidak ada data";
          listGrades=[-1];
          range = statKec.kasus__max-statKec.kasus__min;
          if ( range>=5){
            listGrades.push(statKec.kasus__min,
                Math.round(0.2*(statKec.kasus__max-statKec.kasus__min)),
                Math.round(0.4*(statKec.kasus__max-statKec.kasus__min)),
                Math.round(0.6*(statKec.kasus__max-statKec.kasus__min)),
                Math.round(0.8*(statKec.kasus__max-statKec.kasus__min)),
                statKec.kasus__max)
          } 
            else{
              for (var i=statKec.kasus__min; i<statKec.kasus__max; i++){
                listGrades.push(i)
              }
            }
          console.log(listGrades)
            var div = L.DomUtil.create('div', 'info legend'),
                grades = listGrades,
                labels = [],
                from, to;
            labels.push('<i style="background:' + getColorKec(nullGrades) + '"></i> ' +
                    nullGrades);
            console.log(grades)
            console.log(grades.length)
            for (var i = 0; i < grades.length; i++) {
                from = grades[i];
                to = grades[i + 1];

                labels.push(
                    '<i style="background:' + getColorKec(from+1) + '"></i> ' +
                      (from+1) + (to ? '&ndash;' + to : '+'));
            }

            div.innerHTML = labels.join('<br>');
            return div;
      };

    map.on('overlayadd', function (eventLayer) {
    // Switch to the Population legend...
    if (eventLayer.name === 'Kecamatan') {
        this.removeControl(legendPkm);
        legendKec.addTo(this);
    } else { // Or switch to the Population Change legend...
        this.removeControl(legendKec);
        legendPkm.addTo(this);
    }
});

  // control that shows state info on hover

  var info = L.control({position: 'bottomleft'});

  console.log(qs.penyakit_query)
  optPenyakit = "Semua Penyakit"; 
  optGender = "Semua Jenis"; 
  optUmur = "Semua Umur"; 
  optDateStart = qs.lastDate;
  optDateEnd = " "; 
  optKasus = "Semua Jenis";

  if (qs.penyakit_query !=null){optPenyakit: qs.penyakit_query}
  console.log(optPenyakit)

    if (qs.gender_query===" "){}
      else {optGender: qs.gender_query}
  console.log(optGender)
    if (qs.umur_query===null){}
      else {optUmur: qs.umur_query}
  console.log(optUmur)
    if (qs.dateStart_query===null){}
      else {optDateStart: qs.dateStart_query}
  console.log(optDateStart)
    if (qs.dateEnd_query===null){}
      else {optDateEnd: qs.dateEnd_query}
  console.log(optDateEnd)
    if (qs.jenisKasus_query===null){}
        else {optKasus: qs.jenisKasus_query}
  console.log(optKasus)

  info.onAdd = function (map) {
    this._div = L.DomUtil.create('div', 'info');
    this.update();
    return this._div;
  };

  info.update = function () {
    this._div.innerHTML = '<h6>Peta Tematik</h6>';
    /*<br/><ul><li><strong><p>Penyakit:</p></strong>'+optPenyakit '</li>'+ '<li><p>Jenis Kelamin :</p>' + optGender '</li></ul>';
    +
     '<b><p>Jenis Kelamin: </p></b>' + optGender '<br />'+
     '<b><p>Umur: </p></b>' + optUmur '<br />'+
     '<b><p>Tanggal: </p></b>' + optDateStart + '-' + optDateEnd'<br />'+
     '<b><p>Jenis Kasus: </p></b>' + optKasus '<br />';*/
  };

  info.addTo(map);

});