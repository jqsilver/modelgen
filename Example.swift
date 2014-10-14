import Foundation

class Example {
	var myDouble: Double
	var myString: String
	init(myDouble: Double, myString: String) {
		self.myDouble = myDouble
		self.myString = myString
	}
}

func ExampleFromJSON(json: NSDictionary)  -> (Example?, NSError?) {
	if (json["myDouble"] is Double) == false {
		let e = NSError(domain:"com.modeljson.error", code:-1, userInfo:["reason":"+invalid myDouble"])
		return (nil, e)
	}
	if (json["myString"] is String) == false {
		let e = NSError(domain:"com.modeljson.error", code:-1, userInfo:["reason":"+invalid myString"])
		return (nil, e)
	}
	return (Example(json["myDouble"] as Double, json["myString"] as String), nil)
}
