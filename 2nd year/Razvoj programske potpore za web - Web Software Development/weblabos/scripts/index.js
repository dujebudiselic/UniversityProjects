document.addEventListener("DOMContentLoaded", function() {
   brojukupnostvariukosari();
   brojpojedinihproizvoda();
});

//kad se stisne kosarica otic na cart.html
function dokosarica() {
   window.location.href = "cart.html";
}

//stvaranje proizvoda
function napraviproizvodzakosaricu(proizvod) {
   const proizvodukosarici = {
       name: proizvod, 
       kolicina: 0
   };
   staviukosaricu(proizvodukosarici);
}

//mjenjanje listu proizvoda nakon sta stisnemo sport
function kategorija(ime)  {
   let kategorija = data.categories.find(function(kategorija) {
      return kategorija.name === ime;
   });
   document.getElementById('kategorija').textContent = ime; 
   for(var i = 1; i < 6; i++) { 
       let imageElement = document.getElementById('slikaproizvoda' + (i));
       document.getElementById('proizvod' + (i)).textContent = kategorija.products[i - 1].name;
       document.getElementById('kategorija' + (i)).textContent = ime;
       imageElement.src = kategorija.products[i - 1].image;
   }
   brojpojedinihproizvoda();
}

//dodavanje kolicina proizvoda
function dodaj(broj) {
   const izabranproizvod = document.getElementById('proizvod' + broj).textContent;
   if(izabranproizvod !== 'Proizvod1' && izabranproizvod !== 'Proizvod2' && izabranproizvod !== 'Proizvod3' && izabranproizvod !== 'Proizvod4' && izabranproizvod !== 'Proizvod5'){
      let brojiproizvode = localStorage.getItem('brojiproizvode');
      brojiproizvode = JSON.parse(brojiproizvode);
      if(brojiproizvode){
         brojiproizvode = brojiproizvode + 1;
         localStorage.setItem('brojiproizvode', brojiproizvode);
      }
      else
      {
         localStorage.setItem('brojiproizvode', 1);
      }
      napraviproizvodzakosaricu(izabranproizvod);
   }
}

//stavljanje u kosaricu
function staviukosaricu(proizvodukosarici) { 
   let proizvodiukosarici = localStorage.getItem('proizvodiukosarici');
   proizvodiukosarici = JSON.parse(proizvodiukosarici);
   if(proizvodiukosarici != null){
        if (proizvodiukosarici[proizvodukosarici.name] === undefined) {
         proizvodiukosarici = {
               ...proizvodiukosarici,
               [proizvodukosarici.name]: proizvodukosarici
           }
       }
       proizvodiukosarici[proizvodukosarici.name].kolicina = proizvodiukosarici[proizvodukosarici.name].kolicina + 1;
   } 
   else 
   {
      proizvodukosarici.kolicina = 1;
       proizvodiukosarici = {
           [proizvodukosarici.name]: proizvodukosarici
       }
   }
   localStorage.setItem("proizvodiukosarici", JSON.stringify(proizvodiukosarici));
   brojukupnostvariukosari();
}

//crveni kruzic kod kosarice
function brojukupnostvariukosari(){
   let brojiproizvode = localStorage.getItem('brojiproizvode');
   brojiproizvode = JSON.parse(brojiproizvode);
   let crvenikosara = document.getElementById('crveni');
   crvenikosara.textContent = brojiproizvode;
   if (brojiproizvode == null || brojiproizvode === 0) {
      crvenikosara.style.opacity = 0;
   } 
   else 
   {
      crvenikosara.style.opacity = 1;
   }
   brojpojedinihproizvoda();
}

//crveni kruzic kod pojedinog proizvoda
function brojpojedinihproizvoda(){
   let brojiproizvode = localStorage.getItem('proizvodiukosarici');
   brojiproizvode = JSON.parse(brojiproizvode);
   for(var i = 1; i < 6; i++) {
       let ime = document.getElementById('proizvod' + (i)).textContent;
       let crvenislika = document.getElementById('crvenislika' + (i));
       //console.log(crvenislika);
       if(brojiproizvode === 0 || brojiproizvode[ime] == null){
         crvenislika.style.opacity = 0;
      }
      else
      {
         crvenislika.textContent = brojiproizvode[ime].kolicina;
         crvenislika.style.opacity = 1;
      }  
   }
}

