import { initializeApp } from "firebase/app";
import { getAuth, GoogleAuthProvider } from "firebase/auth";
import { getFirestore } from "firebase/firestore";

const firebaseConfig = {
  apiKey: "AIzaSyCVcme1JGFFld_c-CL38YDbV_JZ31Y8AoU",
  authDomain: "wivisyc.firebaseapp.com",
  projectId: "wivisyc",
  storageBucket: "wivisyc.firebasestorage.app",
  messagingSenderId: "90359493516",
  appId: "1:90359493516:web:b418d3aaba685037a7dca9"
};

const app = initializeApp(firebaseConfig);

export const auth = getAuth(app);
export const provider = new GoogleAuthProvider();
export const db = getFirestore(app);