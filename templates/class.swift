import Foundation

class {{classname}} {
    {% for prop_name, prop_type in properties.items() %}
    	var {{prop_name}}: {{prop_type}}
    {% endfor %} 

    init({{ properties.items()|map('formatForArgument')|join(", ")}}) {
    {% for prop_name in properties.keys() %}
    	self.{{prop_name}} = {{prop_name}}
    {% endfor %} 
    }

    class func fromJSON(json: NSDictionary) -> ({{classname}}?, NSError?) {
       	// validate keys
	    {% for json_key, prop_name in json_key_to_property.items() %}
    	{% set prop_type = properties[prop_name] %}
    	if !(json["{{ json_key }}"] is {{prop_type}}) {
    		let userInfo = ["reason": "{{json_key}} is not {{prop_type}}"]
    		let e = NSError(domain:"com.modeljson.error", code:-1, userInfo:userInfo)
    		return (nil, e)
    	}
	    {% endfor %} 

        // Use keys with unsafe cast
        return ({{classname}}(
           {{json_key_to_property.items()|map('formatForArgumentWithCast')|join(", ")}}
        ), nil)
    }

    func toJSON() -> NSDictionary {
        return [
            {% for json_key, prop_name in json_key_to_property.items() %}
            "{{json_key}}": self.{{prop_name}},
            {% endfor %}
        ];
    }
}

