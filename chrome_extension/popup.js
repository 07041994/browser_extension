// document.getElementById('captureBtn').addEventListener('click', async () => {
//   const tabs = await chrome.tabs.query({});

//   // collect first 3 tab URLs
//   const urls = tabs.slice(0, 3).map(tab => tab.url);

//   fetch("http://127.0.0.1:8000/screenshot", {
//     method: "POST",
//     headers: {
//       "Content-Type": "application/x-www-form-urlencoded"
//     },
//     body: new URLSearchParams({
//       "request": urls
//     })
//   })
//   .then(res => res.json())
//   .then(data => alert("Screenshot request initiated"))
//   .catch(err => console.error(err));
// });

// document.getElementById('captureBtn').addEventListener('click', async () => {
//   try {
//     // get all open tabs in the current window
//     const tabs = await chrome.tabs.query({});
//     const urls = tabs.map(tab => tab.url).filter(url => !!url);

//     if (urls.length === 0) {
//       alert("No open tabs found!");
//       return;
//     }

//     console.log("Sending URLs to backend:", urls);

//     fetch("http://127.0.0.1:8000/screenshot", {
//       method: "POST",
//       headers: {
//         "Content-Type": "application/x-www-form-urlencoded"
//       },
//       body: new URLSearchParams({
//         "request": urls
//       })
//     })
//     .then(res => res.json())
//     .then(data => alert("Screenshot request initiated for " + urls.length + " tabs"))
//     .catch(err => {
//       console.error(err);
//       alert("Error sending screenshot request");
//     });

//   } catch (err) {
//     console.error("Error reading tabs:", err);
//   }
// });

document.getElementById('captureBtn').addEventListener('click', async () => {
  try {
    // Get all open tabs
    const tabs = await chrome.tabs.query({});
    const urls = tabs.map(tab => tab.url).filter(url => !!url);

    if (urls.length === 0) {
      alert("No open tabs found!");
      return;
    }

    // Build URLSearchParams with repeated "request" keys
    const params = new URLSearchParams();
    urls.forEach(url => params.append("request", url));

    console.log("Sending URLs to backend:", urls);

    fetch("http://127.0.0.1:8000/screenshot", {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded"
      },
      body: params
    })
    .then(res => res.json())
    .then(data => {
      alert(`Screenshot request initiated for ${urls.length} tabs`);
      console.log("Server response:", data);
    })
    .catch(err => {
      console.error("Error sending request:", err);
      alert("Error initiating screenshot request");
    });

  } catch (err) {
    console.error("Error reading tabs:", err);
    alert("Unable to read browser tabs");
  }
});
