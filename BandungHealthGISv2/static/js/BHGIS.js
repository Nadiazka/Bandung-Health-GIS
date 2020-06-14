$(document).ready(function(){
 
    //MAPPING//
    var Layer1 = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
    {attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'});
    var Layer2 = L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_nolabels/{z}/{x}/{y}{r}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>'});
/*
    URLpkm = "static/data/areaPkm.geojson";
    URLkec = "static/data/areaKec.geojson";
    URLtpkm = "static/data/titikPkm.geojson";
*/
      // load GeoJSON from an external file
URLpkm = "https://raw.githubusercontent.com/Nadiazka/TugasAkhir/master/trialv12/data/areaPkm.geojson";
URLkec = "https://raw.githubusercontent.com/Nadiazka/TugasAkhir/master/trialv12/data/areaKec.geojson";
URLtpkm = "https://raw.githubusercontent.com/Nadiazka/TugasAkhir/master/trialv12/data/titikPkm.geojson";


    var dataPuskesmas = {} ;
    var dataStatPkm = {};
    var dataKecamatan = {} ;
    var dataStatKec = {};
    var dataChartPkm = {};
    var dataChartKec = {};
    var dataChartPnykt = {};
    var dataChartGender = {};
    var dataChartUmur = {};
    var dataChartPeriode = {};
    var dataClustering = [];

    //FILTERING //
	 $("#filter").submit(function(){
        alert("Masuk Pak Haji")
        $.ajax({
            //url: "/CobaView01/",
            
            url: "/index/",
            //url: "/MainView/", /* URL hasil */
            type:'GET',
            data:{
                penyakit_query:$('#InputPnykt').val(),
                gender_query:$('#InputGender').val(),
                umur_query:$('#InputUmur').val(),
                dateStart_query:$('#dateStart').val(),
                dateEnd_query:$('#dateEnd').val(),
                jenisKasus_query:$('#InputJenisKasus').val(),
            },
            success: function(data){
                alert($('#InputPnykt').val())
                alert($('#InputGender').val())
                alert($('#InputUmur').val())
                alert($('#dateStart').val())
                alert($('#dateEnd').val())
                alert($('#InputJenisKasus').val())

                alert("Oke Nadia")
                alert(data)
                data1 = [data.areaPkm[0].kode_pkm]
                alert(data1)
                alert("ada lagi nih")
                data2 = [data.areaKec[0].kat_pasien]
                alert(data2)

            // MAPPING //
            //Puskesmas
            for (var i = 0; i < data.areaPkm.length; i++) {
                  dataPuskesmas[data.areaPkm[i].kode__kode_pkm] = {"area" : data.areaPkm[i].kode__kode_pkm__nama_pkm, "kasus" : data.areaPkm[i].kasus};
              };
            dataStatPkm = data.StatPkm;

            //Kecamatan
            for (var i = 0; i < data.areaKec.length; i++) {
                  dataKecamatan[data.areaKec[i].kode__kode_pkm__kode_kec] = {"area" : data.areaKec[i].kode__kode_pkm__kode_kec__nama_kec, "kasus" : data[i].kasus};
              };
            dataStatKec = data.StatKec; 


            // DIAGRAM //
            //Puskesmas
            for (var i = 0; i < data.chartPkm.length; i++) {
                dataChartPkm["label"] = data.chartPkm[i].kode__kode_pkm__nama_pkm;
                dataChartPkm["data"] = data[i].kasus;
              };

            //Kecamatan
            for (var i = 0; i < data.chartKec.length; i++) {
                dataChartKec["label"] = data.chartKec[i].kode__kode_pkm__kode_kec__nama_kec;
                dataChartKec["data"] = data[i].kasus;
              };

            //Penyakit
            for (var i = 0; i < data.chartPenyakit.length; i++) {
                dataChartPnykt["label"] = data.chartPenyakit[i].icd_10__nama_subkat;
                dataChartPnykt["data"] = data.chartPenyakit[i].kasus;
              };

            //Gender
            for (var i = 0; i < data.chartGender.length; i++) {
                dataChartGender["label"] = data.chartGender[i].kat_pasien__jenis_kelamin;
                dataChartGender["data"] = data.chartGender[i].kasus;
              };

            //Umur
            for (var i = 0; i < data.chartUmur.length; i++) {
                dataChartUmur["label"] = data.chartUmur[i].kat_pasien__umur;
                dataChartUmur["data"] = data.chartUmur[i].kasus;
              };

            //Periode
            for (var i = 0; i < data.chartPeriode.length; i++) {
                dataChartPeriode["label"] = data.chartPeriode[i].kode__tanggal;
                dataChartPeriode["data"] = data.chartPeriode[i].kasus;
              };

            // CLUSTERING //
            for (var i = 0; i < data.dataClustering.length; i++) {
                dataClustering[i] = data.dataClustering[i];
              };

            },
            error : function(error_data){
                alert("Data tidak tersedia")
            }
        })
    });

console.log(dataPuskesmas);
console.log(dataKecamatan);
console.log(dataStatPkm);
console.log(dataStatKec);
console.log(dataChartPkm);
console.log(dataChartKec);
console.log(dataChartPnykt);
console.log(dataChartGender);
console.log(dataChartUmur);
console.log(dataChartPeriode);

    //general fitur
    function getColor(d) {
          return d > 200  ? '#800026' :
                  d > 100 ? '#BD0026' :
                  d > 50  ? '#E31A1C' :
                  d > 25  ? '#FC4E2A' :
                  d > 10  ? '#FD8D3C' :
                  d > 5   ? '#FEB24C' :
                           '#FFEDA0';
      }

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
    var LayerPkm = L.layerGroup();

    function stylePkm(feature) {
      console.log(feature.properties.kode_kode);
        return {
              fillColor: getColor(dataPuskesmas[feature.properties.kode_kode].kasus),
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

    $.getJSON(URLpkm,function(data){
      console.log(data);
        L.geoJson(data, {
        style: stylePkm,
        onEachFeature: onEachFeaturePkm
        }).addTo(LayerPkm);
    });


    //Kecamatan
    var LayerKec = L.layerGroup();
    function styleKec(feature) {
        return {
              fillColor: getColor(dataKecamatan[feature.properties.kode_kode].kasus),
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
    var legend = L.control({position: 'bottomright'});

      legend.onAdd = function (map) {

          var div = L.DomUtil.create('div', 'info legend'),
              grades = [0, 5, 10, 25, 50, 100, 200, 500],
              labels = [],
              from, to;

          for (var i = 0; i < grades.length; i++) {
              from = grades[i];
              to = grades[i + 1];

              labels.push(
                  '<i style="background:' + getColor(from + 1) + '"></i> ' +
                  from + (to ? '&ndash;' + to : '+'));
          }

          div.innerHTML = labels.join('<br>');
          return div;
      };

    legend.addTo(map);

    //DIAGRAM//
    //Puskesmas
    var cPkm = document.getElementById("ChartPkm").getContext('2d');
    var myChartPkm = new Chart(cPkm, {
      type: 'bar',
      data: {
        labels: dataChartPkm.label,
        datasets: [{
          label: 'Kasus',
          data: dataChartPkm.data,
          backgroundColor: 'rgba(54, 162, 235, 0.2)',
          borderColor: 'rgba(54, 162, 235, 1)', 
          borderWidth: 1
          }]
        },
      options: {
        responsive : true,
        legend: {
            position: 'bottom',
          },
        title: {
          display: true,
          text: 'Top 10 Puskesmas'
        },
        scales: {
          yAxes: [{
            ticks: {
            beginAtZero: true
            }
          }]
        }
      }
    });

    //Kecamatan
    var cKec = document.getElementById("ChartKec").getContext('2d');
    var myChartKec = new Chart(cKec, {
      type: 'bar',
      data: {
        labels: dataChartKec.label,
        datasets: [{
          label: 'Kasus',
          data: dataChartKec.data,
          backgroundColor: 'rgba(75, 192, 192, 0.2)',
          borderColor: 'rgba(75, 192, 192, 1)', 
          borderWidth: 1
          }]
        },
      options: {
        responsive : true,
        legend: {
            position: 'bottom',
          },
        title: {
          display: true,
          text: 'Top 10 Kecamatan'
        },
        scales: {
          yAxes: [{
            ticks: {
            beginAtZero: true
            }
          }]
        }
      }
    });

    //Penyakit
    var cPnykt = document.getElementById("ChartPenyakit").getContext('2d');
    var myChartPnykt = new Chart(cPnykt, {
      type: 'bar',
      data: {
        labels: dataChartPnykt.label,
        datasets: [{
          label: 'Kasus',
          data: dataChartPnykt.data,
          backgroundColor: 'rgba(54, 162, 235, 0.2)',
          borderColor: 'rgba(54, 162, 235, 1)', 
          borderWidth: 1
          }]
        },
      options: {
        responsive : true,
        legend: {
            position: 'bottom',
          },
        title: {
          display: true,
          text: 'Diagram Penyakit'
        },
        scales: {
          yAxes: [{
            ticks: {
            beginAtZero: true
            }
          }]
        }
      }
    });

    //Gender
    var cGender = document.getElementById("ChartGender").getContext('2d');
    var myChartGender = new Chart(cGender, {
      type: 'pie',
      data: {
        labels: dataChartGender.label,
        datasets: [{
          label: 'Kasus',
          data: dataChartGender.data,
          backgroundColor: ['rgba(153, 102, 255, 0.2)', 'rgba(255, 99, 132, 0.2)'],
          borderColor: ['rgba(153, 102, 255, 1)', 'rgba(255,99,132,1)'],  
          borderWidth: 1
          }]
        },
      options: {
        responsive : true,
        legend: {
            position: 'bottom',
          },
        title: {
          display: true,
          text: 'Gender Persentase'
        }
      }
    });

    //Umur
    var cUmur = document.getElementById("ChartUmur").getContext('2d');
    var myChartUmur = new Chart(cUmur, {
      type: 'bar',
      data: {
        labels: dataChartUmur.label,
        datasets: [{
          label: 'Kasus',
          data: dataChartUmur.data,
          backgroundColor: 'rgba(255, 206, 86, 0.2)',
          borderColor: 'rgba(255, 206, 86, 1)', 
          borderWidth: 1
          }]
        },
      options: {
        responsive : true,
        legend: {
            position: 'bottom',
          },
        title: {
          display: true,
          text: 'Diagram Umur'
        },
        scales: {
          yAxes: [{
            ticks: {
            beginAtZero: true
            }
          }]
        }
      }
    });

    //Periode
    var cPer = document.getElementById("ChartPeriode").getContext('2d');
    var myChartPeriode = new Chart(cPer, {
      type: 'line',
      data: {
        labels: dataChartPeriode.label,
        datasets: [{
          label: 'Kasus',
          data: dataChartPeriode.data,
          backgroundColor: 'rgba(255, 159, 64, 0.2)',
          borderColor: 'rgba(255, 159, 64, 1)', 
          borderWidth: 1
          }]
        },
      options: {
        responsive : true,
        legend: {
            position: 'bottom',
          },
        title: {
          display: true,
          text: 'Grafik Periode'
        },
        scales: {
          yAxes: [{
            ticks: {
            beginAtZero: true
            }
          }]
        }
      }
    })

});