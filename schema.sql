DROP TABLE IF EXISTS users;

CREATE TABLE users(
    user_id TEXT PRIMARY KEY,
    password TEXT NOT NULL
);

DROP TABLE IF EXISTS admins;
CREATE TABLE admins(
    admin_id TEXT PRIMARY KEY,
    password TEXT NOT NULL
);
INSERT INTO admins(admin_id,password)
VALUES('admin',123);

DROP TABLE IF EXISTS jewels;

CREATE TABLE jewels(
    jewel_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price  REAL NOT NULL,
    type TEXT NOT NULL,
    gender TEXT,
    description TEXT,
    stock REAL NOT NULL
);

INSERT INTO jewels(name,price,type,gender,description,stock)
VALUES('HENRYKA',40.92,"necklace","female","Sterling silver and natural Garnet necklace",5),
      ('GINKGO',58.8,"earrings","female",'fGinkgo leaf shape, with Chinese ancient style, niche style, Gold-plated earrings',2),
      ('JOWISDM',500.72,"ring","female",'925 Sterling Silver Stackable Ring with 3A Cubic Zirconia,Jewellery for Women',8),
      ('PEARALL',400.95,"ring","male","Temperament simple high-grade sense K gold natural pearl ring",30),
      ('LUNARON',600.58,"necklace","female","Golden necklace,Light luxury fashion angel necklace",30),
      ('GLIMM',99.82,"earrings","female","Fancy earrings that give you shine",9),
       ('HETIANJADE',550,"necklace","male","fancy jade necklace white jade peace buckle jade pendant",3),
       ('ERDING',28.8,"earrings","male","Sterling silver stud earrings, very creative and style stud earrings",3),
       ('JOLLYS',358.8,"bracelet","female","Beautifully designed authentic White Gold ladies bracelet. Perfect for a wife, girlfriend, fiance, sister or mum. ",5),
       ('JANES',2674,"ring","female","Wedding diamond ring, with top design, this is your best choice. ",2),
       ('JANESWEET',38,"earrings","female","Good design, gold plated earrings, cute style.",200),
       ('BLOSSOM',128,"bracelet","female","A luxurious bracelet",20);

DROP TABLE IF EXISTS orders;

CREATE TABLE orders(
    order_id INTEGER,
    user_id INTEGER NOT NULL,
    jewel_id  INTEGER NOT NULL,
    jewel_name TEXT NOT NULL,
    jewel_price REAL NOT NULL,
    order_sum REAL NOT NULL,
    phone TEXT NOT NULL,
    address TEXT,
    number INTEGER NOT NULL
);
    
SELECT * FROM orders;

