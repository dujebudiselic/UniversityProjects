const express = require('express');
const cart_router = express.Router();

cart_router.get('/cart', (req, res) => {
  let kosarica;
  if (req.session.kosarica) {
    kosarica = req.session.kosarica;
  } else {
    kosarica = [];
  }
  res.render('cart', {kosarica});
});

cart_router.get('/cart/getAll', (req, res) => {
    res.redirect('/cart');
});

cart_router.get('/cart/add/:id', (req, res) => {
  const id = req.params.id;
  console.log(id);
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
  let proizvod = kosarica.find(function(proizvod) {
    return proizvod.id === id;
  });
  if (proizvod) {
    proizvod.kolicina++;
  } else {
    kosarica.push({ id: id, kolicina: 1 });
  }
  ukupno++;
  req.session.ukupno = ukupno;
  req.session.kosarica = kosarica;
  res.redirect('back'); 
});

cart_router.get('/cart/remove/:id', (req, res) => {
  let id = req.params.id;
  //console.log('++++++++++++++++++++++++++++++')
  console.log(id);
  let ukupno;
  if (req.session.ukupno) {
    ukupno = req.session.ukupno;
  } else {
    ukupno = 0;
  }
  //console.log(ukupno);
  let kosarica;
  if (req.session.kosarica) {
    kosarica = req.session.kosarica;
  } else {
    kosarica = [];
  }
  let proizvod = kosarica.find(function(proizvod) {
    return proizvod.id === id;
  });
  if(proizvod){
    proizvod = kosarica.find(function(proizvod) { return proizvod.id === id;});
  } else {
    proizvod = {};
  }
  //console.log(proizvod);
  if (proizvod) {
    proizvod.kolicina--;
    if (proizvod.kolicina <= 0) {
        kosarica = kosarica.filter(function(proizvod) {
            return proizvod.id !== id;
        });
    }
    req.session.kosarica = kosarica;
  }
  ukupno--;
  req.session.ukupno = ukupno;
  res.redirect('back');
});

cart_router.get('/cart/removeAll', (req, res) => {
  let ukupno = 0;
  let kosarica = [];
  req.session.ukupno = ukupno;
  req.session.kosarica = kosarica;
  res.redirect('back');
});

module.exports = cart_router;