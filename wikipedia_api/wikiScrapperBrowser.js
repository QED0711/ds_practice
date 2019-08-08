const https = require('https');
const request = require("request")

const DomParser = require('dom-parser')
const parser = new DomParser();

function getNextSibling(node){
    /*
    This takes a starting node searches for the next "ul" tag after this node.
    That "ul" tag can be either a sibling to the starting node or a child of a sibling. 
    */

    // if it is a ul, we found it and return it     
    if(node.nodeName === "UL") return node
    
    // If we encounter a div, check to see if it has a child ul.
    // If so, return that ul. If not, move on to next sibling.      
    if(node.nodeName === "DIV" && node.classList.value === "div-col columns column-width"){
        let divContents = node.getElementsByTagName("ul"); 
        let divHasUL =  divContents.length > 0
        return divHasUL ? divContents[0] : getNextSibling(node.nextSibling)
    } 
    return getNextSibling(node.nextSibling)
}

function getLinks(ul){
    const children = ul.children
    let links = []
    for (let child of children){
        if(child.nodeName === "LI"){
            links.push(child.children[0].href)
        }
    }
    return links
}

function getCloseLinks(html){
    let seeAlsoLinks;
    try{
        seeAlsoLinks = html.getElementById("See_also").parentNode    
    } catch(err){
        return null
    }
    debugger
    const ul = getNextSibling(seeAlsoLinks)
    return getLinks(ul)


}


request.get("https://en.wikipedia.org/wiki/GitHub", (err, res, body) => {
    
    debugger
    const html = parser.parseFromString(body)

    return getCloseLinks(html)
})

// https.get("https://en.wikipedia.org/wiki/GitHub", res => {
//     console.log(res)
// })

