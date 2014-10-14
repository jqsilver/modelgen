#!/bin/python
import json


def printClass(class_json):
    props = class_json["properties"]
    print class_json["class_type"] + " " + class_json["classname"] + " {"
    for property in props.items():
        print "\tvar " + property[0] + ": " + property[1]

    init_args = [property[0] + ": " + property[1] for property in props.items()]
    print "\tinit("+", ".join(init_args)+") {"
    for prop_name in props.keys():
        print "\t\tself."+prop_name+" = "+prop_name
    print "\t}"
    
    print "}"

def validateMapping(class_json, json_to_property):
    mapped_properties = json_to_property.values()
    for prop_name in class_json["properties"].keys():
        if prop_name not in mapped_properties:
            print "// missing "+prop_name
            return False
    return True


def printDeserializer(class_json, json_key_to_property):
    classname = class_json["classname"]
    props = class_json["properties"]

    # function declaration
    print "func "+classname+"FromJSON(json: NSDictionary)",
    print " -> ("+classname+"?, NSError?) {"

    # property type checks
    for json_key, prop_name in json_key_to_property.items(): 
        prop_type = props[prop_name]
        print "\tif (json[\""+json_key+"\"] is "+prop_type+") == false {"
        reason = "[\"reason\":\"invalid "+json_key+"\"]"
        print "\t\tlet e = NSError(domain:\"com.modeljson.error\", code:-1, userInfo:"+reason+")"
        print "\t\treturn (nil, e)"
        print "\t}"

    # then instantiate it with forced casts
    args_with_casts = [prop_name+": json[\""+json_key+"\"]" + " as " + props[prop_name] for (json_key, prop_name) in json_key_to_property.items()]
    print "\treturn ("+classname+"("+", ".join(args_with_casts)+"), nil)"
    print "}"

raw_json_string = open('./example/ExampleSpec.json', 'r').read()
example_json = json.loads(raw_json_string)
raw_mapping_string = open('./example/ExampleMapping.json', 'r').read()
json_key_to_property = json.loads(raw_mapping_string)

if not validateMapping(example_json, json_key_to_property):
    print "// Missing required properties in mapping"

print "import Foundation"
print
printClass(example_json)
print
printDeserializer(example_json, json_key_to_property)
