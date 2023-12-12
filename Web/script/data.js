const ctx = document.getElementById('myChart');
const apiUrl = 'https://061jbi0hu6.execute-api.ap-northeast-1.amazonaws.com/prod/air/bulk';
const buttons = document.getElementsByClassName('button');
let Chartobji;
async function foo(){
  let obj;
  let databody;
  const res = await fetch(apiUrl);
  obj = await res.json();
  databody = obj['body']['Items'];

  ctx.height = 500;
  var chartobj = new Chart(ctx, {
    type: 'line',
    data: {
      labels: databody.map((o) => new Date(o.timestamp*1000).toTimeString().split(' ')[0]).reverse(),
      datasets: [{
        label: 'Temp',
        data: databody.map(o => o.temp).reverse(),
        parsing: {
          yAxisKey: 'temp'
        }
      },{
        label: 'Humid',
        data: databody.map(o => o.humid).reverse(),
        parsing: {
          yAxisKey: 'humid'
        }
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        x: {gridLines: { color: "#131c2b" }},
        y: {gridLines: { color: "#131c2b" }}
      }
    }
  });
  
  Chartobji = chartobj
}
foo();

for(var i = 0; i < buttons.length; i++){
  buttons[i].addEventListener("click", function() {
    for(var j = 0; j < buttons.length; j++){
      buttons[j].classList.remove('clicked');
    }
    this.classList.add('clicked');
  
    if(this.id.split('-')[2]=='all'){
      btnall();
    } else if(this.id.split('-')[2]=='tem') {
      btntem();
    } else if(this.id.split('-')[2]=='hum') {
      btnhum();
    } else if(this.id.split('-')[2]=='upd'){
      this.classList.remove('clicked');
      buttons[0].classList.add('clicked');
      remove_chart();
      foo();
    }
  }, false);
}

function remove_chart(){
  Chartobji.destroy();
}
function btnall(){
  Chartobji.getDatasetMeta(1).hidden = false;
  Chartobji.getDatasetMeta(0).hidden = false;
  Chartobji.update();
}
function btntem(){
  Chartobji.getDatasetMeta(1).hidden = true;
  Chartobji.getDatasetMeta(0).hidden = false;
  Chartobji.update();
}
function btnhum(){
  Chartobji.getDatasetMeta(1).hidden = false;
  Chartobji.getDatasetMeta(0).hidden = true;
  Chartobji.update();
}
