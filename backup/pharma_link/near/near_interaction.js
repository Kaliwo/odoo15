const { connect, KeyPair, utils } = require("near-api-js");
const fs = require("fs");

// Load the NEAR configuration
const nearConfig = JSON.parse(fs.readFileSync("near_config.json", "utf8"));

// Initialize the NEAR connection
async function initNearConnection() {
  const near = await connect(nearConfig);
  return near;
}

// Function to store encrypted data on the NEAR blockchain
async function storeEncryptedData(accountId, data, privateKey) {
  const near = await initNearConnection();
  const keyPair = KeyPair.fromString(privateKey);
  const account = await near.account(accountId);

  const contract = new utils.Contract(account, accountId, {
    viewMethods: [],
    changeMethods: ["store_data"],
    sender: accountId,
  });

  await contract.store_data({ data }, 300000000000000, utils.format.parseNearAmount("0.1"));
}

// Function to retrieve encrypted data from the NEAR blockchain
async function retrieveEncryptedData(accountId, privateKey) {
  const near = await initNearConnection();
  const keyPair = KeyPair.fromString(privateKey);
  const account = await near.account(accountId);

  const contract = new utils.Contract(account, accountId, {
    viewMethods: ["get_data"],
    changeMethods: [],
    sender: accountId,
  });

  const data = await contract.get_data();
  console.log(data);
}

// Main function to handle incoming operation requests
async function main(operation, ...args) {
  if (operation === "store") {
    await storeEncryptedData(...args);
  } else if (operation === "retrieve") {
    await retrieveEncryptedData(...args);
  } else {
    console.error("Invalid operation");
  }
}

main(...process.argv.slice(2)).catch(console.error);
