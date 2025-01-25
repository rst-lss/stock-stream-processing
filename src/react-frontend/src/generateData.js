function generateDataArray() {
  const dataArray = [];
  const currentUnixTimestamp = Math.floor(Date.now() / 1000); // Current timestamp in seconds
  let prevClose = 100.0; // Initial close value

  for (let i = 0; i < 100; i++) {
    const timestamp = currentUnixTimestamp + i * 86400; // Increment by 1 day (86400 seconds)
    const open = prevClose; // Set open to previous close

    // Random variation for high and low
    const high = open + Math.random() * 5; // Random high value
    const low = open - Math.random() * 5; // Random low value

    // Random close value: sometimes higher, sometimes lower
    const close = Math.random() < 0.5 ? open - Math.random() * 5 : open + Math.random() * 5;

    dataArray.push([timestamp * 1000, open, close, low, high]); // Multiply timestamp by 1000 for milliseconds
    prevClose = close; // Update prevClose for the next iteration
  }

  return dataArray;
}
export default generateDataArray;
