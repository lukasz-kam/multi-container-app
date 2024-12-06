db = db.getSiblingDB('admin');
db.auth('ADMIN_USER', 'ADMIN_PASSWORD');

db = db.getSiblingDB("todos");
db.createUser({
    user: "USER_TO_CHANGE",
    pwd: "PASS_TO_CHANGE",
    roles: [ { role: "dbOwner", db: "todos" } ]
});
