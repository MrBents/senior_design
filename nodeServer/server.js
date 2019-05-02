const express = require('express');
const bodyParser = require('body-parser');
const expressValidator = require('express-validator');
const port = process.env.PORT || 8000;

var admin = require("firebase-admin");
var queue = '';

var serviceAccount = require("../serviceAccountKey.json");

admin.initializeApp({
    credential: admin.credential.cert(serviceAccount),
    databaseURL: "https://seniordesign-a35a7.firebaseio.com"
});

const db = admin.firestore();
const settings = {/* your settings... */ timestampsInSnapshots: true };
db.settings(settings);

const app = express();
app.use(express.static('public'))
app.use(bodyParser.urlencoded({ extended: false }));

app.get('/changeProb', function (req, res, next) {
    console.log(req.query.name);
    names = req.query.name
    values = req.query.value
    id = req.query.id
    probabilities = []
    for (i = 0; i < names.length; i++) {
        probabilities.push({ name: names[i], value: values[i] })
    }
    console.log(probabilities);
    db.collection('Customer').doc(id).update({
        probabilities: probabilities
    }).then(e => '');
    res.send(
        {
            message: 'Hello from server!!',
        });
});

app.get('/getName', function (req, res, next) {
    //queue.push(req.query.name);
    console.log(req.query.name)
    queue = req.query.name
    var time = new Date()
    hour = time.getHours()
    emojis = ['Chicken Sandwich', 'Nuggets', 'Spicy Deluxe Sandwich']
    var min = 0;
    var max = 2;
    var random = Math.floor(Math.random() * (+max - +min)) + +min;
    console.log(req.query.new);
    if (req.query.new == 'true' || req.query.name == 'nikhil') {
        db.collection('Customer').doc(req.query.name).set({
            age: req.query.age,
            ethnicity: req.query.ethnicity,
            face_id: req.query.name,
            gender: req.query.gender,
            inLine: true,
            probabilities: [
                {
                    name: req.query.beverage,
                    value: 1
                },
                {
                    name: req.query.food,
                    value: 1
                },
                {
                    name: req.query.side,
                    value: 1
                }
            ]
        })
    } else {
        db.collection('Customer').doc(req.query.name).update({
            inLine: true,
        })
    }
    db.collection('Histograms').doc('patronCount').get().then(function (doc) {
        hours = doc.data()['hours'];
        hours[hour] = hours[hour] + 1;
    }).then(function () {
        db.collection('Histograms').doc('patronCount').update({
            hours: hours
        })
    })
});

app.get('/giveName', function (req, res, next) {
    //var i = queue.shift(); // queue is now [5]
    //console.log(i)
    console.log(queue)
    // if (queue.length == 0) {
    //     queue = [i]
    // }
    res.send(
        {
            name: queue,
        });
});

app.listen(port, function () {
    console.log('Server started!');
});