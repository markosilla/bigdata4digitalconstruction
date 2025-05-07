const fs = require("fs");

const fullHash = process.env.VERCEL_GIT_COMMIT_SHA || "{{GIT_HASH}}";
const hash = fullHash.substring(0, 7);
const filePath = "src/index.html";
const html = fs.readFileSync(filePath, "utf8");
const result = html.replace("{{GIT_HASH}}", hash);
fs.writeFileSync(filePath, result);

console.log(`Injected git hash "${hash}" into ${filePath}`);
