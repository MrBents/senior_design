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
      var that = this;
      firestore.collection('Customer').where("inLine", "==", true)
        .onSnapshot(function (snapshot) {
          var customers = {};
          var features = {};
          snapshot.forEach(function (doc) {
            var probs = doc.data()['probabilities']
            customers[doc.data()['face_id']] = probs
            features[doc.data()['face_id']] = [doc.data()['age'], doc.data()['gender'], doc.data()['ethnicity']]
          });
          console.log(customers)
          const keys = Object.keys(customers)
          console.log(keys)
          var i = 1;
          var compList = keys.map((id) =>
            <div className="border">
              <div className="App2">
                <text>FaceID: {id}</text>
                <text>Age: {features[id][0]}</text>
                <text>Gender: {features[id][1]}</text>
                <text>Ethnicity: {features[id][2]}</text>
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
    yAxis: {
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
