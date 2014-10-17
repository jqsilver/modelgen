import Foundation

class {{classname}} {
    {% for prop_name, prop_type in properties.items() %}
    	var {{prop_name}}: {{prop_type}}
    {% endfor %} 

    init({{arg_list}}) {
    {% for prop_name in properties.keys() %}
    	self.{{prop_name}} = {{prop_name}}
    {% endfor %} 
    }

    class func fromJSON(json: NSDictionary) -> ({{classname}}?, NSError?) {
       	// validate keys
	    {% for json_key, prop_name in json_mapping.items() %}
    	{% set prop_type = properties[prop_name] %}
    	if !(json["{{ json_key }}"] is {{prop_type}}) {
    		let userInfo = ["reason": "{{json_key}} is not {{prop_type}}"]
    		let e = NSError(domain:"com.modeljson.error", code:-1, userInfo:userInfo)
    		return (nil, e)
    	}
	    {% endfor %} 
	    return ({{classname}}({{init_args_with_casts}}), nil)
    }
}

