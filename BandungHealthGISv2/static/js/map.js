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
dataPuskesmas={}
URLdataPuskesmas = "static/data/dataPuskesmas.json";
$.getJSON(URLdataPuskesmas, function(data){
  for (var i = 0; i < areaPkm.length; i++) {
    dataPkm[areaPkm[i].kode__kode_pkm] = {
      "area" : areaPkm[i].kode__kode_pkm__nama_pkm,
      "kasus" : areaPkm[i].kasus
    };
  };
  dataPuskesmas = $.extend(data, dataPkm)
})

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
	L.geoJson(data, {
	style: stylePkm,
	onEachFeature: onEachFeaturePkm
	}).addTo(LayerPkm);
});


//Kecamatan
dataKec = {}
dataKecamatan = {}
URLdataKecamatan = "static/data/dataKecamatan.json";
$.getJSON(URLdataKecamatan, function(data){
  console.log(data)
  for (var i = 0; i < areaKec.length; i++) {
    dataKec[areaKec[i].kode__kode_pkm__kode_kec] = {
      "area" : areaKec[i].kode__kode_pkm__kode_kec__nama_kec, 
      "kasus" : areaKec[i].kasus
    };
  };
  dataKecamatan = $.extend(data, dataKec)
})

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
console.log(qsClustering)
var Clustering1 = L.layerGroup();
var Clustering2 = L.layerGroup();
var Clustering3 = L.layerGroup();

if (qsClustering[0] != null && qsClustering[0] != undefined ){
  var strClust1 = qsClustering[0].klaster_kode
  var dataClust1 = strClust1.split(", ")
  var strNamaClust1 = qsClustering[0].klaster_nama
  var namaClust1 = strNamaClust1.split(", ")

  function highlightFeatureClstr1(e) {
    console.log("Masuk highlightFeatureClstr1")
    var layer = e.target;
    if (!L.Browser.ie && !L.Browser.opera && !L.Browser.edge) {
              layer.bringToFront();
            }
    var out = [];
    out.push("Kecamatan : "+namaClust1[i]);
    out.push("Penyakit : "+qsClustering[0].subkat__nama_subkat);
    out.push("Jenis Kelamin : "+qsClustering[0].jenis_kelamin);
    out.push("Tanggal : "+qsClustering[0].tanggal);
    out.push("Derajat Signifikansi : "+ qsClustering[0].llr);
    layer.bindPopup(out.join("<br />"));
    layer.on('mouseover', function (e) {
          this.openPopup();
          });
    layer.on('mouseout', function (e) {
        this.closePopup();
    });
    
    }

  function onEachFeatureClstr1(feature, layer) {
    layer.on({
        mouseover: highlightFeatureClstr1,
        click: zoomToFeature
    });
    layer.bindPopup("Kecamatan : "+namaClust1[i])
  }

  $.getJSON(URLkec,function(data){
      console.log(data);
      for (var i = 0; i < dataClust1.length; i++) {
        L.geoJson(data, {
          filter : function (feature){
            if (feature.properties.kode_kode=== dataClust1[i]) return true;
          },
          style : function(feature){
            if (feature.properties.kode_kode=== dataClust1[i]) return {color: "#1e0505"};
          },
          onEachFeature: onEachFeatureClstr1
        }).addTo(Clustering1);
      }
      console.log("clustering aman")
    });
}

if (qsClustering[1] != null && qsClustering[1] != undefined ){
  var strClust2 = qsClustering[1].klaster_kode
  var dataClust2 = strClust2.split(", ")
  var strNamaClust2 = qsClustering[1].klaster_nama
  var namaClust2 = strNamaClust2.split(", ")

  function highlightFeatureClstr2(e) {
    console.log("Masuk highlightFeatureClstr1")
    var layer = e.target;
    if (!L.Browser.ie && !L.Browser.opera && !L.Browser.edge) {
              layer.bringToFront();
            }
    var out = [];
    out.push("Kecamatan : "+namaClust2[i]);
    out.push("Penyakit : "+qsClustering[1].subkat__nama_subkat);
    out.push("Jenis Kelamin : "+qsClustering[1].jenis_kelamin);
    out.push("Tanggal : "+qsClustering[1].tanggal);
    out.push("Derajat Signifikansi : "+ qsClustering[1].llr);
    layer.bindPopup(out.join("<br />"));
    layer.on('mouseover', function (e) {
          this.openPopup();
          });
    layer.on('mouseout', function (e) {
        this.closePopup();
    });
    
    }

  function onEachFeatureClstr2(feature, layer) {
    layer.on({
        mouseover: highlightFeatureClstr2,
        click: zoomToFeature
    });
  }
  
  $.getJSON(URLkec,function(data){
      console.log(data);
      for (var i = 0; i < dataClust2.length; i++) {
        L.geoJson(data, {
          filter : function (feature){
            if (feature.properties.kode_kode=== dataClust2[i]) return true
          },
          style : function(feature){
            if (feature.properties.kode_kode=== dataClust2[i]) return {color: "#472103"};
          },
          onEachFeature: onEachFeatureClstr2
        }).addTo(Clustering2);
    }
      console.log("clustering aman")
    });
}
  
if (qsClustering[2] != null && qsClustering[2] != undefined ){
  var strClust3 = qsClustering[2].klaster_kode
  var dataClust3 = strClust3.split(", ")
  var strNamaClust3 = qsClustering[2].klaster_nama
  var namaClust3 = strNamaClust3.split(", ")

  function highlightFeatureClstr3(e) {
    console.log("Masuk highlightFeatureClstr1")
    var layer = e.target;
    if (!L.Browser.ie && !L.Browser.opera && !L.Browser.edge) {
              layer.bringToFront();
            }
    var out = [];
    out.push("Kecamatan : "+namaClust3[i]);
    out.push("Penyakit : "+qsClustering[2].subkat__nama_subkat);
    out.push("Jenis Kelamin : "+qsClustering[2].jenis_kelamin);
    out.push("Tanggal : "+qsClustering[2].tanggal);
    out.push("Derajat Signifikansi : "+ qsClustering[2].llr);
    layer.bindPopup(out.join("<br />"));
    layer.on('mouseover', function (e) {
          this.openPopup();
          });
    layer.on('mouseout', function (e) {
        this.closePopup();
    });
    
    }

  function onEachFeatureClstr3(feature, layer) {
    layer.on({
        mouseover: highlightFeatureClstr3,
        click: zoomToFeature
    });
  }
  
  $.getJSON(URLkec,function(data){
      console.log(data);
      for (var i = 0; i < dataClust3.length; i++) {
        L.geoJson(data, {
          filter : function (feature){
            if (feature.properties.kode_kode=== dataClust3[i]) return true
          },
          style : function(feature){
            if (feature.properties.kode_kode=== dataClust3[i]) return {color: "#403803"};
          },
          onEachFeature: onEachFeatureClstr3
        }).addTo(Clustering3);
    }
      console.log("clustering aman")
    });
}

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
      "Clustering 1" : Clustering1,
      "Clustering 2" : Clustering2,
      "Clustering 3" : Clustering3,
	};

	L.control.layers(baseMaps, overlayMaps, {position:'topleft'}).addTo(map);

	//Legenda
	  var legendPkm = L.control({position: 'bottomright'});

	      legendPkm.onAdd = function (map) {
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
	          var div = L.DomUtil.create('div', 'info legend'),
	              grades = listGrades,
	              labels = [],
	              from, to;
            labels.push('<i style="background:' + getColorPkm(nullGrades) + '"></i> ' +
                    nullGrades);
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
            var div = L.DomUtil.create('div', 'info legend'),
                grades = listGrades,
                labels = [],
                from, to;
            labels.push('<i style="background:' + getColorKec(nullGrades) + '"></i> ' +
                    nullGrades);
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

  optPenyakit = "Semua Penyakit"; 
  optGender = "Semua Jenis"; 
  optUmur = "Semua Umur"; 
  optDateStart = qs.startPeriode;
  optDateEnd = qs.endPeriode; 
  optKasus = "Semua Jenis";
  optClust = [];

  if (qs.penyakit_query != null && qs.penyakit_query != undefined){
    optPenyakit = qs.penyakit_query
  }
  
  for (var i=0; i<qsClustering.length; i++){
    optClust[i]=qsClustering[i].subkat__nama_subkat
    }
  
  if (qs.gender_query != null && qs.gender_query != undefined){
    optGender = qs.gender_query
  }

  if (qs.umur_query != null && qs.umur_query != undefined){
    optUmur = qs.umur_query
  }

  if (qs.startPeriode != null && qs.startPeriode != undefined){
    optDateStart = qs.startPeriode
  }

  if (qs.endPeriode != null && qs.endPeriode != undefined){
    optDateEnd = qs.endPeriode
  }

  if (qs.dateEnd_query != null && qs.dateEnd_query != undefined){
    optDateEnd = qs.dateEnd_query
  }

  if (qs.jenisKasus_query != null && qs.jenisKasus_query != undefined){
    optKasus = qs.jenisKasus_query
  }

  if (qs.dateEnd_query != null && qs.dateEnd_query != undefined){
    optDateEnd = qs.dateEnd_query
  }

  if (qs.dateEnd_query != null && qs.dateEnd_query != undefined){
    optDateEnd = qs.dateEnd_query
  }

  info.onAdd = function (map) {
    this._div = L.DomUtil.create('div', 'info');
    this.update();
    return this._div;
  };

  info.update = function () {
    this._div.innerHTML = '<h6>Data terpilih</h6>'+
    '<br/><ul><li><p><strong>Penyakit : </strong>'+ optPenyakit +'</p></li>'+
    '<li><p><strong>Jenis Kelamin : </strong>' + optGender +'</p></li>'+
    '<li><p><strong>Umur : </strong>' + optUmur +'</p></li>'+
    '<li><p><strong>Periode : </strong>' + optDateStart + ' <strong>-</strong> ' + optDateEnd +'</p></li>'+
    '<li><p><strong>Jenis Kasus : </strong>' + optKasus +'</p></li>'+
    '<li><p><strong>Clustering 1 : </strong>' + optClust[0] +'</p></li>'+
    '<li><p><strong>Clustering 2 : </strong>' + optClust[1] +'</p></li>'+
    '<li><p><strong>Clustering 3 : </strong>' + optClust[2] +'</p></li></ul>';
  };

  info.addTo(map);

});