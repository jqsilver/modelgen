#!/bin/python
import json

def printClass(class_json):
    props = class_json["properties"]
    print class_json["class_type"] + " " + class_json["classname"] + " {"
    for property in props:
        print "\tvar " + property[0] + ": " + property[1]

    init_args = [property[0] + ": " + property[1] for property in props]
    print "\tinit("+", ".join(init_args)+") {"
    for p in props:
        print "\t\tself."+p[0]+" = "+p[0]
    print "\t}"
    
    print "}"

def printDeserializer(class_json):
    classname = class_json["classname"]
    props = class_json["properties"]

    print "func "+classname+"FromJSON(json: NSDictionary)",
    print " -> ("+classname+"?, NSError?) {"
    # first validate the arguments
    for prop in props: 
        print "\tif (json[\""+prop[0]+"\"] is "+prop[1]+") == false {"
        reason = "[\"reason\":\"+invalid "+prop[0]+"\"]"
        print "\t\tlet e = NSError(domain:\"com.modeljson.error\", code:-1, userInfo:"+reason+")"
        print "\t\treturn (nil, e)"
        print "\t}"
    # then instantiate it with forced casts
    args_with_casts = ["json[\""+prop[0]+"\"]" + " as " + prop[1] for prop in props]
    print "\treturn ("+classname+"("+", ".join(args_with_casts)+"), nil)"
    print "}"
    
    
raw_json_string = open('./example/ExampleSpec.json', 'r').read()
example_json = json.loads(raw_json_string)

print "import Foundation"
print
printClass(example_json)
print
printDeserializer(example_json)
