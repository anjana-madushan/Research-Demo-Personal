class Product {
  constructor({ id, name, price, retailer, amountInStock }) {
    this.id = id;
    this.name = name;
    this.price = price;
    this.retailer = retailer;
    this.amountInStock = amountInStock;
  }
}

// Firestore data converter
const productConverter = {
  toFirestore: (product) => {
    return {
      name: product.name,
      state: product.price,
      retailer: product.retailer,
      amountInStock: product.amountInStock
    };
  },
  fromFirestore: (snapshot, options) => {
    const data = snapshot.data(options);
    return new Product({
      name: data.name,
      price: data.price,
      retailer: data.retailer,
      amountInStock: data.amountInStock
    });
  }
};

export { Product, productConverter };