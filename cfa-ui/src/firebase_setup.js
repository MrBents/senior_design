import firebase from '@firebase/app';
import 'firebase/firestore';
const firebaseConfig = {
    apiKey: "AIzaSyApDwn8JAzGaUBECIP_I5HfwfU_Lc0kVII",
    authDomain: "seniordesign-a35a7.firebaseapp.com",
    databaseURL: "https://seniordesign-a35a7.firebaseio.com",
    projectId: "seniordesign-a35a7",
    storageBucket: "seniordesign-a35a7.appspot.com",
    messagingSenderId: "493618574545"
}

const Firebase = firebase.initializeApp(firebaseConfig);
export default Firebase;