// parameterizing dotenv variables for easy use in other files
import dotenv from "dotenv";
dotenv.config();

export default {
  port: process.env.PORT,
  fire_apiKey: process.env.FIRE_APIKEY,
  fire_authDomain: process.env.FIRE_AUTH_DOMAIN,
  fire_projectId: process.env.FIRE_PROJECT_ID,
  fire_storageBucket: process.env.FIRE_STORAGE_BUCKET,
  fire_messagingSenderId: process.env.FIRE_MESSAGING_SENDER_ID,
  fire_appId: process.env.FIRE_APP_ID
}
