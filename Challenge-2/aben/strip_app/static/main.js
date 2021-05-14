console.log("Sanity check!");
// new
// Get Stripe publishable key

fetch("/config/")
.then((result) => { return result.json(); })
.then((data) => {
  debugger
  // Initialize Stripe.js
  const stripe = Stripe(data.publicKey);
  // new
  let submitBtn = document.querySelector("#submitBtn");
  // Event handler
  if (submitBtn !== null) {
    submitBtn.addEventListener("click", () => {
    // Get Checkout Session ID
    fetch("/create-checkout-session/")
      .then((result) => { return result.json(); })
      .then((data) => {
        console.log(data);
        // Redirect to Stripe Checkout
        return stripe.redirectToCheckout({sessionId: data.sessionId})
      })
      .then((res) => {
        console.log(res);
      });
    });
  }
});