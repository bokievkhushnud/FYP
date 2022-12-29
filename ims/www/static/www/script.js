
// var html5QrcodeScanner = new Html5QrcodeScanner(
// 	"reader", { fps: 10, qrbox: 250 });
let scan = document.getElementById("scanqr")
let stop_scan = document.getElementById("closeqr")
let stop_scan1 = document.getElementById("closeqr1")
// function onScanSuccess(decodedText, decodedResult) {
//     // Handle on success condition with the decoded text or result.
//     console.log(`Scan result: ${decodedText}`);
//     // console.log(`http://127.0.0.1:8000/${decodedText}/`)
//     window.location = `http://127.0.0.1:8000/${decodedText}/`;
//     html5QrcodeScanner.clear();
//     // ^ this will stop the scanner (video feed) and clear the scan area.
// }
// html5QrcodeScanner.render(onScanSuccess);


// function onScanError(errorMessage) {
//     // handle on error condition, with error message

// }
const html5QrCode = new Html5Qrcode(/* element id */ "reader");




scan.addEventListener('click', () => {
  // This method will trigger user permissions
  Html5Qrcode.getCameras().then(devices => {
    if (devices && devices.length) {
      console.log(devices.length)
      var cameraId = devices[devices.length-1].id;
      html5QrCode.start(
        cameraId,
        {
          fps: 10,
          facingMode: "environment",
          // qrbox: { width: 200, height: 200 }  // Optional, if you want bounded box UI
        },
        (decodedText, decodedResult) => {
          html5QrCode.stop().then((ignore) => {
            console.log("QR Code scanning is ")
            // QR Code scanning is stopped.
          }).catch((err) => {
            // Stop failed, handle it.
          });
          window.location = `https://invenotry-ms.herokuapp.com/${decodedText}/`;
        },
        (errorMessage) => {
          // parse error, ignore it.
        })
        .catch((err) => {
          // Start failed, handle it.
        });
    }
  }).catch(err => {
    // handle err
  });

  stop_scan.addEventListener('click', () => {
    html5QrCode.stop().then((ignore) => {
      console.log("QR Code scanning is ")
      // QR Code scanning is stopped.
    }).catch((err) => {
      // Stop failed, handle it.
    });
  })
  stop_scan1.addEventListener('click', () => {
    html5QrCode.stop().then((ignore) => {
      console.log("QR Code scanning is ")
      // QR Code scanning is stopped.
    }).catch((err) => {
      // Stop failed, handle it.
    });
  })

})

// File based scanning
const fileinput = document.getElementById('qr-input-file');
fileinput.addEventListener('change', e => {
  if (e.target.files.length == 0) {
    // No file selected, ignore 
    return;
  }
  const imageFile = e.target.files[0];
  // Scan QR Code
  html5QrCode.scanFile(imageFile, true)
    .then(decodedText => {
      window.location = `http://127.0.0.1:8000/${decodedText}/`;
      console.log(decodedText);
    })
    .catch(err => {
      // failure, handle it.
      console.log(`Error scanning file. Reason: ${err}`)
    });
});


