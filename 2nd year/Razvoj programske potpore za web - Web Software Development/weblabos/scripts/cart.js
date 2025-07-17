document.addEventListener("DOMContentLoaded", function() {
   kosarica();
});

//kad se stisne gumb otic na index.html
function doglavne() {
   window.location.href = "index.html";
}

//prikaz sta  je u kosarici
function kosarica() {
   let proizvodiukosarici = localStorage.getItem('proizvodiukosarici');
   proizvodiukosarici = JSON.parse(proizvodiukosarici);
   let kosarica = document.querySelector("#listakosarice");
   if (kosarica && proizvodiukosarici) { 
      kosarica.innerHTML = "";
      let sadrzajkosarice = "";
      Object.values(proizvodiukosarici).map(function(item) {
         sadrzajkosarice = sadrzajkosarice + `
         <div id="proizvod">
             <div>
                 <span>${item.name}</span>
             </div>
             <div>
                 <span onclick="smanjibrojproizvoda(this)" id="minus"> - </span>
                 <span>${item.kolicina}</span>
                 <span onclick="povecajbrojproizvoda(this)" id="plus"> + </span>
             </div>
         </div>
         `;
      });
      kosarica.innerHTML = sadrzajkosarice;
   }
}

//minus gumb
function smanjibrojproizvoda(element){
   let roditelj = element.parentNode.parentNode;
   let djeca = roditelj.querySelector('span').innerText;
   let proizvodiukosarici = localStorage.getItem('proizvodiukosarici');
   proizvodiukosarici = JSON.parse(proizvodiukosarici);
   let brojiproizvode = localStorage.getItem('brojiproizvode');
   brojiproizvode = JSON.parse(brojiproizvode);
   brojiproizvode = brojiproizvode - 1;
   localStorage.setItem('brojiproizvode', brojiproizvode);
   proizvodiukosarici[djeca].kolicina = proizvodiukosarici[djeca].kolicina - 1;
   if(proizvodiukosarici[djeca].kolicina === 0){
      delete proizvodiukosarici[djeca];
      alert("Proizvod ste izbacili iz košare")
   }
   localStorage.setItem('proizvodiukosarici', JSON.stringify(proizvodiukosarici));
   kosarica();
}

//plus gumb
function povecajbrojproizvoda(element){
   let roditelj = element.parentNode.parentNode;
   let djeca = roditelj.querySelector('span').innerText;
   let proizvodiukosarici = localStorage.getItem('proizvodiukosarici');
   proizvodiukosarici = JSON.parse(proizvodiukosarici);
   let brojiproizvode = localStorage.getItem('brojiproizvode');
   brojiproizvode = JSON.parse(brojiproizvode);
   brojiproizvode = brojiproizvode + 1;
   localStorage.setItem('brojiproizvode', brojiproizvode);
   proizvodiukosarici[djeca].kolicina = proizvodiukosarici[djeca].kolicina + 1;
   //if(proizvodiukosarici[djeca].kolicina >= 100){
   //   alert("Previše komada jednog proizvoda");
   //}
   localStorage.setItem('proizvodiukosarici', JSON.stringify(proizvodiukosarici));
   kosarica();
}

//brisanje kosarice
function izbrisisveukosarici(){
   localStorage.clear();
   localStorage.setItem('brojiproizvode', 0);
   localStorage.setItem('proizvodiukosarici', '{}');
   kosarica();
}