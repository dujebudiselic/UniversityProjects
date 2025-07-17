const express = require('express');
const home_Routes = require('./routes/home.routes.js');
const cart_Routes = require('./routes/cart.routes.js');
const session = require('express-session');

const app = express();

app.set('view engine', 'ejs');

app.use(session({
  secret: 'bilosto',
  resave : false,
  cookie : { maxAge : 24 * 60 * 60 * 1000},
  //cookie: {maxAge: 10000},
  saveUninitialized : true,
}));

app.use(express.static('public'));

app.use(home_Routes);
app.use(cart_Routes);

app.get('/', (req, res) => {
  res.redirect('/home');
})

app.listen(3000, () => {
  console.log('Server is running on port 3000');
});
