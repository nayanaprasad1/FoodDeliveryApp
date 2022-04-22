import sqlite3
con=sqlite3.connect("projectDB.db")
#print("Database created successfully")

#con.execute("drop table users")
#con.execute("create table users(user_id integer primary key autoincrement, name text not null, gender text not null, email text not null, phone text not null, password text not null);")

# con.execute("DELETE FROM users WHERE email = 'abc@gmail.com';")
#res=con.execute("select * from users")
#for i in res:
#    print(i[0],i[1],i[2],i[3],i[4],i[5])

#con.execute('drop table products')
#con.execute("create table products(id integer primary key autoincrement, name text not null, image text not null, price float not null, onSale integer, onSalePrice float not null, kind text not null);")
#
#con.execute("INSERT INTO products (name,image,price,onSale,onSalePrice,kind) VALUES (?,?,?,?,?,?) ", ("Rice","rice.jpg",250,0,250,'veg'))
#con.execute("INSERT INTO products (name,image,price,onSale,onSalePrice,kind) VALUES (?,?,?,?,?,?) ", ("Paneer","paneer.jpg",300,1,300,'veg'))
#con.execute("INSERT INTO products (name,image,price,onSale,onSalePrice,kind) VALUES (?,?,?,?,?,?) ", ("Mushroom","mushroom.jpg",200,0,200,'veg'))
#con.execute("INSERT INTO products (name,image,price,onSale,onSalePrice,kind) VALUES (?,?,?,?,?,?) ", ("Mix-Veg","mixveg.jpg",100,0,100,'veg'))
#con.execute("INSERT INTO products (name,image,price,onSale,onSalePrice,kind) VALUES (?,?,?,?,?,?) ", ("Dal Makhani","dal.jpg",60,0,60,'veg'))
#con.execute("INSERT INTO products (name,image,price,onSale,onSalePrice,kind) VALUES (?,?,?,?,?,?) ", ("Paw Bhaji","powbhaji.jpg",150,1,150,'veg'))

#
#con.execute("INSERT INTO products (name,image,price,onSale,onSalePrice,kind) VALUES (?,?,?,?,?,?) ", ("Chicken","chicken.jpg",500,1,500,'nonveg'))
#con.execute("INSERT INTO products (name,image,price,onSale,onSalePrice,kind) VALUES (?,?,?,?,?,?) ", ("Mutton","mutton.jpg",600,0,600,'nonveg'))
#con.execute("INSERT INTO products (name,image,price,onSale,onSalePrice,kind) VALUES (?,?,?,?,?,?) ", ("Fish","fish.jpg",200,0,200,'nonveg'))
#con.execute("INSERT INTO products (name,image,price,onSale,onSalePrice,kind) VALUES (?,?,?,?,?,?) ", ("Prawn Fish","prawn.jpg",500,1,500,'nonveg'))
#con.execute("INSERT INTO products (name,image,price,onSale,onSalePrice,kind) VALUES (?,?,?,?,?,?) ", ("Egg Dish","egg.jpg",100,1,100,'nonveg'))

#
#con.execute("INSERT INTO products (name,image,price,onSale,onSalePrice,kind) VALUES (?,?,?,?,?,?) ", ("Paani Puri","panipuri.jpg",250,0,250,'snacks'))
#con.execute("INSERT INTO products (name,image,price,onSale,onSalePrice,kind) VALUES (?,?,?,?,?,?) ", ("Paneer Tikka","paneertika.jpg",100,0,100,'snacks'))
#con.execute("INSERT INTO products (name,image,price,onSale,onSalePrice,kind) VALUES (?,?,?,?,?,?) ", ("Onion Salad","onionsalad.jpg",45,1,45,'snacks'))
#con.execute("INSERT INTO products (name,image,price,onSale,onSalePrice,kind) VALUES (?,?,?,?,?,?) ", ("Momos","momos.jpg",100,0,100,'snacks'))

#
#con.execute("INSERT INTO products (name,image,price,onSale,onSalePrice,kind) VALUES (?,?,?,?,?,?) ", ("Butter Naan","butternaan.jpg",70,0,70,'bread'))
#con.execute("INSERT INTO products (name,image,price,onSale,onSalePrice,kind) VALUES (?,?,?,?,?,?) ", ("Naan","naan.jpg",40,1,40,'bread'))
#con.execute("INSERT INTO products (name,image,price,onSale,onSalePrice,kind) VALUES (?,?,?,?,?,?) ", ("Roti","roti.jpg",40,0,40,'bread'))
#con.execute("INSERT INTO products (name,image,price,onSale,onSalePrice,kind) VALUES (?,?,?,?,?,?) ", ("Paratha","paratha.jpg",100,1,100,'bread'))
#con.execute("INSERT INTO products (name,image,price,onSale,onSalePrice,kind) VALUES (?,?,?,?,?,?) ", ("Kulcha","kulcha.jpg",100,0,100,'bread'))
#con.execute("INSERT INTO products (name,image,price,onSale,onSalePrice,kind) VALUES (?,?,?,?,?,?) ", ("Aloo Paratha","alooparatha.jpg",200,1,200,'bread'))

#
#con.execute("INSERT INTO products (name,image,price,onSale,onSalePrice,kind) VALUES (?,?,?,?,?,?) ", ("Rasogulla","rasgulla.jpg",30,0,30,'sweets'))
#con.execute("INSERT INTO products (name,image,price,onSale,onSalePrice,kind) VALUES (?,?,?,?,?,?) ", ("Gulab Jamun","gulab.jpg",25,1,25,'sweets'))
#con.execute("INSERT INTO products (name,image,price,onSale,onSalePrice,kind) VALUES (?,?,?,?,?,?) ", ("Ice Cream","ice1.jpg",50,0,50,'sweets'))
#con.execute("INSERT INTO products (name,image,price,onSale,onSalePrice,kind) VALUES (?,?,?,?,?,?) ", ("Cone","ice2.jpg",150,0,150,'sweets'))

#

#con.execute("INSERT INTO products (name,image,price,onSale,onSalePrice,kind) VALUES (?,?,?,?,?,?) ", ("Pepsi","pepsi.jpg",100,1,100,'bevarages'))
#con.execute("INSERT INTO products (name,image,price,onSale,onSalePrice,kind) VALUES (?,?,?,?,?,?) ", ("Coca Cola","coke.jpg",60,0,60,'bevarages'))
#con.execute("INSERT INTO products (name,image,price,onSale,onSalePrice,kind) VALUES (?,?,?,?,?,?) ", ("7Up","7up.jpg",40,1,40,'bevarages'))
#con.execute("INSERT INTO products (name,image,price,onSale,onSalePrice,kind) VALUES (?,?,?,?,?,?) ", ("Water","water.jpg",20,1,20,'bevarages'))
#con.commit()

#res=con.execute("SELECT * FROM products")
#for i in res:
#    print(i[0],i[1],i[2],i[3],i[4],i[5],i[6])

#con.execute("create table cart(image text,name text,qty integer, price text, subTotal text, id integer );")

# con.execute('drop table purchases')
#con.execute("create table purchases(uid integer, name text, image text, quantity integer, id integer, date text);")
#con.commit()


#res=con.execute("SELECT * FROM users")
#for i in res:
#    print(i[0],i[1],i[2],i[3],i[4])


#con.execute('drop table deliveryDetails')
#con.execute("create table deliveryDetails(uid integer, name text, mobile text, ddate text, mail text, method text, address text);")
#con.commit()

#print("Deliveries database created")

#res=con.execute("SELECT * FROM deliveryDetails")
#for i in res:
#    print(i[0],i[1],i[2],i[3],i[4],i[5],i[6])














#con.execute("create table contact(contact_id integer primary key autoincrement , name text not null, number text not null, city text not null, email text not null, query text not null);")
#print("contact table created successfully")

#res=con.execute("select * from contact")
#for i in res:
#    print(i[0],i[1],i[2],i[3])

#con.execute("create table jobs(job_id integer primary key autoincrement, name text not null,number text not null,description text not null);")
#print("Job Seeker table created successfully")

#res=con.execute("select * from jobs")
#for i in res:
#    print(i[0],i[1],i[2],i[3])



#con.execute("create table deliveryin(deliveryboy_id integer primary key autoincrement, name text not null,email text not null, password text not null);")
#print("Delivery Login table created successfully")


#res=con.execute("select * from deliveryin")
#for i in res:
#    print(i[0],i[1],i[2],i[3])





