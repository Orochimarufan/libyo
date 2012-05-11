#!/usr/bin/python3
#@switch (not-quite-)statement
#C 2012 Orochimarufan

class switch(object):
	""" Switch/Case
	
	there are two Versions of this Statement:
		for case in switch(v): 
			if case("hello"):
				do_something
				case.end		# ignore all further cases
			if case():
				do_default
			do_finally			# called wether or not case.end was encountered [WARNING: this is NOT a try...finally replacement!]
	or:
		with switch(v) as case:
			if case("hello"):
				do_something
				case.end		# break out
			if case():
				do_default
			do_else				# called only if no case.end was encountered (yet)
	
	to do real breaking in the for annotation, use 'break' instead of 'case.end'. you could also use "case.end;break;"
	return ...; will ALWAYS BREAK! The do_finally of the for annotation is NOT EXEMPT from that
	"""
	def __init__(this,value):
		this._value = value;
	def __enter__(this):
		f=this.case(this._value);
		f.__with__=True;
		return f;
	def __exit__(this,et,ev,tb):
		if et == StopIteration:
			return True;
	def __iter__(this):
		yield this.case(this._value);
		raise StopIteration;
	class case(object):
		""" A case Statement:
			if case(...):
				do_something
		other uses:
			if case.type(my_type):
				do_something			# if type(value)==my_type
			if case.expr(expr_str):
				do_something			# if expr_str eval()s to true; expr_str will be string.format()ed with value
			if case.func(fn):
				do_something			# if fn(value) evaluates to true; e.g: case.func(lambda v: v-22+3==5)
		"""
		def __init__(this,value):
			this.value = value;
			this.type = type(value);
			this.__with__ = False;
			this.__fall__ = False;
			this.__next__ = True;
		def __dofall__(this):
			if not this.__next__: return False;
			if this.__fall__: return True;
			return None;
		def __rtfall__(this,b):
			if b:
				this.__fall__ = True;
			return b;
		def __call__(this,*other):
			f = this.__dofall__();
			return (f if f is not None else not other or this.__rtfall__(this.value in other));
		def __contains__(this,other):
			f = this.__dofall__();
			return (f if f is not None else this.__rtfall__(other in this.value));
		def expr(this,expr):
			f = this.__dofall__();
			return (f if f is not None else this.__rtfall__(eval(expr.format(this.value))));
		def func(this,fn):
			f = this.__dofall__();
			return (f if f is not None else this.__rtfall__(fn(this.value)));
		def type(this,typ):
			f = this.__dofall__();
			return (f if f is not None else this.__rtfall__(this.type is typ));
		@property
		def end(this):
			this.__next__=False;
			if this.__with__:
				raise StopIteration;
			# we cannot 'break' a for loop from inside here!
			return StopIteration;

def test():
	with switch(1) as case:
		if case.func(lambda x: x==1):
			print("true")
			case.end
		print("false")