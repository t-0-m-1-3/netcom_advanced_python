
var express    = require('express');
var bodyParser = require('body-parser');
var app        = express();
var session    = require('cookie-session');
var csrf    = require('csrf');

app.use(csrf());
app.use(bodyParser());

var port     = process.env.PORT || 8080; // set our port

var mongoose   = require('mongoose');
mongoose.connect('mongodb://127.0.0.1/todos'); // connect to our database
var Todos     = require('./app/models/todo');

var router = express.Router();


router.use(function(req, res, next) {
	console.log('Working.');
	next();
});


router.get('/', function(req, res) {
	res.sendfile('todos.html')
});


router.route('/todos')

	.post(function(req, res) {
		var todo = new Todos();	
		todo.text = req.body.text;  
		todo.details = req.body.details;
		todo.done = true;
		todo.save(function(err) {
			if (err)
				res.send(err);
			res.json(todo);
		});	
	})
	.get(function(req, res) {
		Todos.find(function(err, _todos) {
			if (err)
				res.send(err);
			var todos = {
				'todos':_todos
			}
			res.json(todos);
		});
	});

router.route('/todos/:_id')
	.post(function(req, res) {
		Todos.remove({
			_id: req.params._id
		}, function(err, _todo) {
			if (err)
				res.send(err);
			var todo = {
				_id: req.params._id
			}
			console.log("--- todo");
			console.log(todo);
			res.json(todo);
		});
	});



app.use('/api', router);


app.listen(port);
console.log('Visit port ' + port);
