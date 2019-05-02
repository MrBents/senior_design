import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';
import ReactEcharts from "echarts-for-react";
import firestore from './firestore.js';
import Card from '@material-ui/core/Card';
import CardContent from '@material-ui/core/CardContent';
import ScrollArea from 'react-scrollbar';
import HorizontalScroll from 'react-scroll-horizontal'
import Paper from '@material-ui/core/Paper';
import ReactCSSTransitionGroup from 'react-addons-css-transition-group';


class App extends Component {
  constructor(props) {
    super(props);
    this.chartdata = [
    ];
    this.state = {
      customers: {},
      compList: [],
      keys: []
    }
  }
  componentDidMount() {
    try {
      var order_output = ["Chicken Sandwich", "Deluxe Sandwich", "Spicy Chicken Sandwich",
        "Spicy Deluxe Sandwich", "Grilled Chicken Sandwich", "Grilled Chicken Club", "Nuggets",
        "Chick-n-Strips", "Grilled Cool Wrap", "Grilled Nuggets", "Chicken Biscuit", "Chick-n-Minis",
        "Egg White Grill", "Bacon, Egg & Cheese Biscuit", "Sausage, Egg & Cheese Biscuit",
        "Buttered Biscuit", "Sunflower Multigrain Bagel", "Hash Browns", "Greek Yogurt Parfait",
        "Fruit Cup", "Chicken, Egg & Cheese Bagel", "Hash Brown Scramble Burrito",
        "Hash Brown Scramble Bowl", "English Muffin", "Bacon, Egg & Cheese Muffin",
        "Sausage, Egg & Cheese Muffin", "Cobb Salad", "Waffle Potato Fries", "Side Salad",
        "Chicken Noodle Soup", "Chicken Tortilla Soup", "Superfood Side", "Buddy's Apple Sauce",
        "Carrot Raisin Salad", "Chicken Salad", "Cole Slaw", "Cornbread", "Waffle Potato Chips",
        "Nugget Kid's Meal", "Chick-n-Strips Kid's Meal", "Grilled Nuggets Kid's Meal",
        "Chocolate Milkshake", "Cookies & Cream Milkshake", "Strawberry Milkshake",
        "Vanilla Milkshake", "Frosted Coffee", "Frosted Lemonade", "Chocolate Chunk Cookie",
        "Icedream Cone", "Frosted Key Lime", "Freshly-Brewed Iced Tea Sweetened", "Lemonade",
        "Coca-Cola", "Dr Pepper", "DASANI Bottled Water", "Honest Kids Apple Juice",
        "Simply Orange", "1% Chocolate Milk", "1% White Milk", "Coffee", "Iced Coffee",
        "Gallon Beverages", "Chick-fil-A Diet Lemonade", "Freshly-Brewed Iced Tea Unsweetened",
        "Chick-fil-A Sauce", "Polynesian Sauce", "Honey Mustard Sauce", "Garden Herb Ranch Sauce",
        "Zesty Buffalo Sauce", "Barbeque Sauce", "Sriracha Sauce"]

      var food = ["Chicken Sandwich", "Deluxe Sandwich", "Spicy Chicken Sandwich",
        "Spicy Deluxe Sandwich", "Grilled Chicken Sandwich", "Grilled Chicken Club", "Nuggets",
        "Chick-n-Strips", "Grilled Cool Wrap", "Grilled Nuggets", "Chicken Biscuit", "Chick-n-Minis",
        "Egg White Grill", "Bacon, Egg & Cheese Biscuit", "Sausage, Egg & Cheese Biscuit",
        "Buttered Biscuit", "Sunflower Multigrain Bagel", "Hash Browns",
        "Fruit Cup", "Chicken, Egg & Cheese Bagel", "Hash Brown Scramble Burrito",
        "Hash Brown Scramble Bowl", "English Muffin", "Bacon, Egg & Cheese Muffin",
        "Sausage, Egg & Cheese Muffin", "Chicken Salad", "Cole Slaw", "Cornbread"]

      var side = ["Waffle Potato Fries", "Side Salad", "Greek Yogurt Parfait", "Chicken Noodle Soup",
        "Chicken Tortilla Soup", "Superfood Side", "Buddy's Apple Sauce", "Waffle Potato Chips"]

      var drink = ["Chocolate Milkshake", "Cookies & Cream Milkshake", "Strawberry Milkshake",
        "Vanilla Milkshake", "Frosted Coffee", "Frosted Lemonade", "Frosted Key Lime", "Freshly-Brewed Iced Tea Sweetened", "Lemonade",
        "Coca-Cola", "Dr Pepper", "DASANI Bottled Water", "Honest Kids Apple Juice",
        "Simply Orange", "1% Chocolate Milk", "1% White Milk", "Coffee", "Iced Coffee",
        "Gallon Beverages", "Chick-fil-A Diet Lemonade", "Freshly-Brewed Iced Tea Unsweetened"]
      var that = this;
      firestore.collection('Customer').where("inLine", "==", true)
        .onSnapshot(function (snapshot) {
          var customers = {};
          var features = {};
          snapshot.forEach(function (doc) {
            var probs = doc.data()['probabilities']
            var maxF = 0;
            var maxB = 0;
            var maxS = 0;
            var maxFood = '';
            var maxBeverage = '';
            var maxSide = '';
            for (i = 0; i < probs.length; i++) {
              if (food.includes(probs[i]['name'])) {
                if (probs[i]['value'] > maxF) {
                  maxFood = probs[i]['name'];
                  maxF = probs[i]['value'];
                }
              } else if (drink.includes(probs[i]['name'])) {
                if (probs[i]['value'] > maxB) {
                  maxBeverage = probs[i]['name'];
                  maxB = probs[i]['value'];
                }
              } else if (side.includes(probs[i]['name'])) {
                if (probs[i]['value'] > maxS) {
                  maxSide = probs[i]['name'];
                  maxS = probs[i]['value'];
                }
              }
            }
            if (maxF == 0) {
              maxFood = 'Nothing'
            }
            if (maxB == 0) {
              maxBeverage = 'Nothing'
            }
            if (maxS == 0) {
              maxSide = 'Nothing'
            }
            console.log(maxFood)
            console.log(maxBeverage)
            console.log(maxSide)

            customers[doc.data()['face_id']] = probs
            features[doc.data()['face_id']] = [doc.data()['age'], doc.data()['gender'], doc.data()['ethnicity'], maxFood, maxSide, maxBeverage]//, doc.data()['initialFood'], doc.data()['initialSide'], doc.data()['initialBeverage']]
          });
          console.log(customers)
          const keys = Object.keys(customers)
          console.log(keys)
          var i = 1;
          var compList = keys.map((id) =>
            <div className="border">
              <div className="App2">
                <text>FaceID: <b>{id}</b></text>
                <text>Age: <b>{features[id][0]}</b></text>
                <text>Gender: <b>{features[id][1]}</b></text>
                <text>Ethnicity: <b>{features[id][2]}</b></text>
                <div className="App4">
                  <text className='App5'><b>Order Prediction</b></text>
                  <text>Predicted Meal: <b>{features[id][3]}</b></text>
                  <text>Predicted Side: <b>{features[id][4]}</b></text>
                  <text>Predicted Beverage: <b>{features[id][5]}</b></text>
                </div>
              </div>
              <ReactEcharts option={that.getOption(customers[id])} style={{ height: 200, flex: 1 }} />
            </div>)
          that.setState({
            customers: customers,
            compList: compList,
            keys: keys
          })
        }, function (error) {
        }
        )
      firestore.collection('Histograms').doc("patronCount")
        .onSnapshot(function (doc) {
          var times = doc.data()['hours'];
          console.log(times)
          that.chartdata = [{
            name: 'Hours',
            type: 'bar',
            data: times
          }]
          that.setState({
            times: times
          })
        })
    } catch (error) {
    }
  }

  getOption = (probs) => ({

    // title: {
    //   text: "JS Front End Frameworks",
    //   x: "center"
    // },
    tooltip: {
      trigger: "item",
      formatter: "{a} <br/>{b} : {c} ({d}%)"
    },
    // legend: {
    //   orient: "vertical",
    //   left: "left",
    //   data: ["React", "Angular", "Vue"]
    // },
    series: [{
      name: "Item probability",
      type: "pie",
      radius: "55%",
      center: ["50%", "60%"],
      data: probs,
      itemStyle: {
        emphasis: {
          shadowBlur: 10,
          shadowOffsetX: 0,
          shadowColor: "rgba(0, 0, 0, 0.5)"
        }
      }
    }]
  });

  getOption2 = () => ({
    title: {
      text: 'CFA Busy Hours',
      textStyle: {
        color: '#fff'
      }
    },
    // toolbox: {
    //           show : true,
    //           feature : {            
    //                       dataView : {show: true, title:'Data View', readOnly: false},            
    //                       magicType : {show: false, title:['line','bar'],type: ['line', 'bar']},            
    //                       restore : {show: true, title:'Restore'},            
    //                       saveAsImage : {show: true, title:"Save As Image"}        
    //                      }    
    //          },    
    tooltip: {
      backgroundColor: 'rgba(250,250,250,0.7)',
      textStyle: {
        color: '#000'
      }
    },
    xAxis: {
      data: ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23"]//this.state.hours
    },
    yAxis: {//this.state.hours
    },
    series: this.chartdata,
    backgroundColor: 'rgba(0, 0, 0, 1)',
    textStyle: {
      color: '#fff'
    },
    color: ['#2b95ff']
  });

  render() {
    return (
      <div className="OutContainer">
        <div className="App3">
          <text>Chick-Fill-A Patron Counting and Order Prediction</text>
        </div>
        <div className="Container">
          <div className="App" >
            {/* {this.state.keys.map((id) => <ReactEcharts option={this.getOption(this.state.customers[id])} style={{ height: 200, flex: 1 }} />)} */}
            {this.state.compList}
          </div>
          <div className="App2">
            <ReactEcharts option={this.getOption2()} style={{ height: 200, flex: 1 }} />
          </div>
        </div>
      </div>
    );
  }
}

export default App;
