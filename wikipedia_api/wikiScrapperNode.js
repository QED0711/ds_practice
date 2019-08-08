const cheerio = require("cheerio")
const request = require("request")

request.get("https://en.wikipedia.org/wiki/GitHub", (err, res, body)=> {
    console.log(body)
})