//Diagram Puskesmas
var ctx = document.getElementById("ChartPkm").getContext('2d');
chartPkmLabel = [];
chartPkmData = [];
for (var i = 0; i < chartPkm.length; i++) {
    chartPkmLabel[i] = chartPkm[i].kode__kode_pkm__nama_pkm;
    chartPkmData[i]=chartPkm[i].kasus
  };
var myChart2 = new Chart(ctx, {
	type: 'bar',
	data: {
		labels:chartPkmLabel ,
		datasets: [{
			label: 'Kasus',
			data: chartPkmData,
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
})

//Diagram Kecamatan
var ctx = document.getElementById("ChartKec").getContext('2d');
chartKecLabel = [];
chartKecData = [];
for (var i = 0; i < chartKec.length; i++) {
    chartKecLabel[i] = chartKec[i].kode__kode_pkm__kode_kec__nama_kec;
    chartKecData[i]=chartKec[i].kasus
  };
var myChart2 = new Chart(ctx, {
	type: 'bar',
	data: {
		labels: chartKecLabel,
		datasets: [{
			label: 'Kasus',
			data: chartKecData,
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
chartPenyakitLabel = [];
chartPenyakitData = [];
for (var i = 0; i < chartPenyakit.length; i++) {
    if (chartPenyakit[i].icd_10__nama_subkat != null && chartPenyakit[i].icd_10__nama_subkat != undefined){
    	chartPenyakitLabel[i] = chartPenyakit[i].icd_10__nama_subkat;
    }
    else if (chartPenyakit[i].kat__nama_kat != null && chartPenyakit[i].kat__nama_kat != undefined){
    	chartPenyakitLabel[i] = chartPenyakit[i].kat__nama_kat
    }
    else{chartPenyakitLabel[i] = chartPenyakit[i].chapter__nama_chapter}
    ;
    chartPenyakitData[i]=chartPenyakit[i].kasus
  };
var myChartPnykt = new Chart(cPnykt, {
  type: 'bar',
  data: {
    labels: chartPenyakitLabel,
    datasets: [{
      label: 'Kasus',
      data: chartPenyakitData,
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

//Diagram Jenis Kelamin
var ctx = document.getElementById("ChartGender").getContext('2d');
chartGenderLabel = [];
chartGenderData = [];
for (var i = 0; i < chartGender.length; i++) {
    chartGenderLabel[i] = chartGender[i].kat_pasien__jenis_kelamin;
    chartGenderData[i]=chartGender[i].kasus
  };
var myChart2 = new Chart(ctx, {
	type: 'pie',
	data: {
		labels: chartGenderLabel,
		datasets: [{
			label: 'Kasus',
			data: chartGenderData,
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
})

//Diagram Umur
var ctx = document.getElementById("ChartUmur").getContext('2d');
chartUmurLabel = [];
chartUmurData = [];
for (var i = 0; i < chartUmur.length; i++) {
    chartUmurLabel[i] = chartUmur[i].kat_pasien__umur;
    chartUmurData[i]=chartUmur[i].kasus
  };
var myChart2 = new Chart(ctx, {
	type: 'bar',
	data: {
		labels: chartUmurLabel,
		datasets: [{
			label: 'Kasus',
			data: chartUmurData,
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
})

//Diagram Periode
var ctx = document.getElementById("ChartPeriode").getContext('2d');
chartPeriodeLabel = [];
chartPeriodeData = [];
for (var i = chartPeriode.length; i <0 ; i--) {
    chartPeriodeLabel[i] = chartPeriode[i].kode__tanggal;
    chartPeriodeData[i]=chartPeriode[i].kasus
  };
var myChart2 = new Chart(ctx, {
	type: 'line',
	data: {
		labels: chartPeriodeLabel,
		datasets: [{
			label: 'Kasus',
			data: chartPeriodeData,
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

//Chart Kasus
var ctx = document.getElementById("ChartKasus").getContext('2d');
chartKasusLabel = Object.keys(chartKasus);
chartKasusData = Object.values(chartKasus);

var myChart2 = new Chart(ctx, {
	type: 'pie',
	data: {
		labels: chartKasusLabel,
		datasets: [{
			label: 'Kasus',
			data: chartKasusData,
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
			text: 'Persentase Kasus'
		}
	}
})