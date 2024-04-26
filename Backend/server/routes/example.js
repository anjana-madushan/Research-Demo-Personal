import { Router } from "express";
const router = Router();

router.route("/create").post(async (req, res) => {
  try {
    const { name, price, retailer, amountInStock } = req.body;

    const newProduct = new Product({
      name,
      price,
      retailer,
      amountInStock
    });
    const docRef = await addDoc(collection(db, "prodcuts").withConverter(productConverter), newProduct);
    console.log("new document created:", docRef.id);

    res.status(200).send({ msg: "success", data: { id: docRef.id } });
  } catch (e) {
    console.error("Error creating product:", e);
    res.status(400).send({ msg: "fail", error: e });
  }
})

