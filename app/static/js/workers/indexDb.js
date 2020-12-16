//prefix of implementation
window.indexedDB = window.indexedDB || window.ozIndexedDB || window.webkitIndexedDB || window.msIndexedDB;

//prefix of window.IDB object
window.IDBTransaction = window.IDBTransaction || window.webkitIDBTransaction || window.msIndexedDBTransaction;
window.IDBKeyRange = window.IDBKeyRange || window.webkitIDBKeyRange || window.msIDBKeyRange;

if(!window.indexedDB){
  window.alert("Please upgrade your browser.")
}

let ticketsData= [
  {category: "Technical",comment: "The network hass a down time ", created: "22/08/20",imageURL: "",priority: "HIGH",status: "OPEN",subject: "network downtime",ticketId: "7fgKSLPudIheGGHp",updated: "23/08/20",username: "postgres"},
  {category: "developer",comment: "the website is down for some reason.",created: "23/08/20",imageURL: "/uploads/TdUFgf9.png",priority: "LOW",status: "OPEN",subject: "website down",ticketId: "wpElcFTw6KupSU9G",updated: "31/08/20",username: "Denis Kibe"}
];
var db;
var tableName = sessionStorage.getItem('status');
var request = window.indexedDB.open("tickets", 2);

request.onerror = function(event){
  console.log("error");
};
request.onsuccess = function(event){
  db = request.result;
  console.log("success: "+db)
};

request.onupgradeneeded= function(event){
  var db = event.target.result;
  var objectStore = db.createObjectStore(tableName, {keyPath: "ticketId"});

    for (var i in ticketsData){
      objectStore.add(ticketsData[i]);
    }
};

function startSearch(){
  var tx = db.transaction(tableName).objectStore(tableName);

  tx.openCursor().onsuccess = function(event){
    var cursor = event.target.result;
    if(cursor)
  }
}
