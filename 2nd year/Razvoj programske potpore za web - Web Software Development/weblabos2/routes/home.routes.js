const express = require('express');
const data = require('../data/mydata.js');


const home_router = express.Router();

home_router.get('/home', (req, res) => {
  let proizvodi = {};
  let ime = 'Kategorija x (trenutno otvorena)'
  let ukupno;
  if (req.session.ukupno) {
    ukupno = req.session.ukupno;
  } else {
    ukupno = 0;
  }
  let kosarica;
  if (req.session.kosarica) {
    kosarica = req.session.kosarica;
  } else {
    kosarica = [];
  }
  res.render('home', {proizvodi, ime, ukupno, kosarica});
});

home_router.get('/home/getCategories', (req, res) => {
  res.redirect('/home');
});

home_router.get('/home/getProducts/:id', (req, res) => {
  const id = req.params.id;
  console.log(id);
  //let ukup = req.session.ukupno;
  //console.log('((((((((((((((((((((');
  //console.log(ukup);
  let ukupno;
  if (req.session.ukupno) {
    ukupno = req.session.ukupno;
  } else {
    ukupno = 0;
  }
  //console.log('))))))))))))))))))))');
  //console.log(ukupno);
  let kosarica;
  if (req.session.kosarica) {
    kosarica = req.session.kosarica;
  } else {
    kosarica = [];
  }
  let kategorija = data.categories.find(function(kategorija) {
    return kategorija.name === id;
  });
  let ime = 'Kategorija ';
  let ime2;
  if (kategorija) {
    ime = ime + kategorija.name;
    ime = ime + ' (trenutno otvorena)'
    ime2 = kategorija.name;
  } else {
    ime = 'KATEGORIJA NE POSTOJI!!!';
  }
  let proizvodi;
  if (kategorija) {
    proizvodi = kategorija.products;
  } else {
    proizvodi = [];
  }
  //console.log('-----------------------------------------------------')
  //console.log(ime);
  //console.log(proizvodi);
  res.render('home', {proizvodi, ime, ime2, ukupno, kosarica});
});

module.exports = home_router;
