import streamlit as st 


st.write("app.js")
st.write("*****************")
st.code('''
         const express = require('express');
const mongoose = require('mongoose');
const User = require('./Users');
const bcrypt = require('bcrypt');


const app =  express();
const bodyParser = require('body-parser');
app.use(bodyParser.urlencoded({extended:true}))
app.set('view engine', 'ejs');

mongoose.connect('mongodb://127.0.0.1:27017/login',{
    useNewUrlParser:true,
    useUnifiedTopology: true,
}).then(console.log("MongoDB Connected")).catch(err=>console.log(err));


app.get("/", (req, res)=>{
    res.send("Hello World");
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, ()=>{
    console.log(`Server is running on port ${PORT}`)
});

app.get('/login', (req, res)=>{
    res.render('login');
});

app.post('/login', async (req,res)=>{
    try{
        console.log(req.body);
        const user = await User.findOne({username: req.body.username})
        if(user)
        {
            const validPassword = await bcrypt.compare(req.body.password, user.password);
            if(validPassword)
            {
                // res.send("Credentials Matched");
                res.redirect('/users');
            }
            else{
                res.send("Incorrect Credentials");
            }
        }
        else
        {
            res.send("User not found");
        }
    }catch(error)
    {
        console.log(error);
        res.send("We are facing an error right now, please try again later.");
    }
})

app.get('/register', (req, res)=>{
    res.render('register');
});

app.post('/register', async(req, res)=>{
    console.log(req.body);
    // console.log(res.body);
    try{
        const hashedPassword = await bcrypt.hash(req.body.password, 10);
        const newUser= new User({
            username: req.body.username,
            password: hashedPassword
        });
        
        await newUser.save();
        res.redirect('/login');
    }catch(error){
        console.log(error);
        res.send('Sorry! Something went wrong');
    }
    
});

app.get('/users', async (req, res)=>{
    try{
        const userlist = await User.find();
        res.render('userlist', {users: userlist});
    }catch(error)
    {
        console.log(error);
        res.send("We are facing an error right now, please try again later.");
    }
});

app.get('/users/edit/:id', async(req, res)=>
{
    try{
        const user = await User.findById(req.params.id);
        console.log(user);
        res.render('edituser', {user:user})
    }catch(error)
    {
        console.log(error);
        res.send("We are facing an error right now, please try again later");
    }
});

app.post('/users/update/:id', async(req, res)=>{
    try{
        const user = await User.findByIdAndUpdate(req.params.id, {
            username : req.body.username
        },{new:true});
        res.redirect('/users');
    }catch(error)
    {
        console.log(error);
        res.send("We are facing an error right now, please try again later.");
    }
});


app.post('/users/delete/:id', async (req, res)=>
{
    try{
        await User.findByIdAndDelete(req.params.id);
        res.redirect('/users');
    }catch(error)
    {
        console.log(error);
        res.send("We are facing an error right now, please try again later.");
    }
})
''')

st.write("*****************")

st.write("login.ejs")
st.write("*****************")
st.code('''
         <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login</title>
</head>
<body>
    <h1>Login</h1>
    <form action="/login" method="POST">
        <input type="text" name="username" placeholder="Username" required><br>
        <input type="password" name="password" placeholder="Password" required><br>
        <button type="submit">Login</button>
        <a href="/register" style="display:inline;">
            <button type="button">Register</button>
        </a>
    </form>
    
</body>
</html>

         ''')

st.write("*****************")
st.write("register.ejs")
st.write("*****************")
st.code('''
         <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Register</title>
</head>
<body>
    <h1>Register</h1>
    <form action="/register" method="POST">
        <input type="text" name="username" placeholder="Username" required><br>
        <input type="password" name="password" placeholder="Password" required><br>
        <button type="submit">Register</button>
        <a href="/login" style="display:inline;">
            <button type="button">Login</button>
        </a>

    </form>
    
</body>
</html>

         ''')

st.write("********************")
st.write("edituser.ejs")
st.write("********************")
st.code('''
         <!DOCTYPE html>

<html>
    <head>
        <meta charset="utf-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <title>Edit User</title>
        <meta name="description" content="">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link rel="stylesheet" href="">
    </head>
    <body>
        <h1>Edit User</h1>
        <form action ='/users/update/<%= user._id %>' method="POST">
            <input type="text" name="username" value="<%= user.username%>" required>
            <button type="submit">Update User</button>
        </form>
        
        
        <script src="" async defer></script>
    </body>
</html>
         ''')

st.write("******************")
st.write("userlist.ejs")
st.write("******************")
st.code('''
         <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>User List</title>
</head>
<body>
    <h1>User List</h1>
    <ul>
        <% users.forEach(function(user) {%>
            <li><%= user.username%></li>
            <form action="/users/edit/<%= user._id%>" method="GET" style="display: inline;">
                <button type="submit">Edit USer</button>
            </form>
            <form action="/users/delete/<%= user._id%>" method="POST" style="display:inline;">
                <button type="submit">Delete</button>
            </form>
        <% });%>
    </ul>
    <a href="/register" style="display:inline">
        <button type="button">Log Out</button>
    </a>
</body>
</html>

         ''')

st.write("*******************")
st.write("deleteuser.ejs")
st.write("*******************")
st.code('''
         <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Delete User</title>
</head>
<body>
    <% users.forEach(function(user){%>
        <li>
            <%= user.username%>
            <form action="/users/delete/<%= user._id %>" method="POST" style="display: inline;">
                <button type="submit"> Delete User </button>
            </form>
        </li>
    <% }); %>
</body>
</html>
         ''')

st.write("********************")
st.write("Users.js")
st.write("********************")
st.code('''
         const mongoose = require('mongoose');

const userSchema = new mongoose.Schema({
    username:{
        type: String,
        require: true,
        unique: true
    },
    password:
    {
        type: String,
        require: true
    }
});

const User = mongoose.model('User', userSchema);
module.exports =  User;
         ''')

st.write("********************")
st.write("package.json")
st.write("********************")
st.code('''
        {
  "name": "login",
  "version": "1.0.0",
  "description": "",
  "main": "index.js",
  "scripts": {
    "test": "echo \"Error: no test specified\" && exit 1"
  },
  "keywords": [],
  "author": "",
  "license": "ISC",
  "dependencies": {
    "bcrypt": "^5.1.1",
    "ejs": "^3.1.9",
    "express": "^4.18.2",
    "mongoose": "^8.1.0",
    "mongosh": "^2.1.1"
  }
}

        ''')

st.write("***************")
st.write("Installation Steps")
st.write("***************")
st.code('''
        npm init -y
        npm install express mongoose bcrypt body-parser ejs
        ''')