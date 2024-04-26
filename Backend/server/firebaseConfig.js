import { initializeApp } from "firebase/app";
import { getFirestore } from "firebase/firestore";
import env from "./config.js";

const firebaseConfig = {
  apiKey: env.fire_apiKey,
  authDomain: env.fire_authDomain,
  projectId: env.fire_projectId,
  storageBucket: env.fire_storageBucket,
  messagingSenderId: env.fire_messagingSenderId,
  appId: env.fire_appId
};

const firebaseApp = initializeApp(firebaseConfig);
const db = getFirestore(firebaseApp);

export default db;