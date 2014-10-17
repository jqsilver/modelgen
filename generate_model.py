#!/bin/python
import json
import jinja2
import string

def getTemplate(name):
    loader = jinja2.FileSystemLoader(searchpath="./templates")
    env = jinja2.Environment(loader=loader, trim_blocks=True, lstrip_blocks=True)
    return env.get_template(name)

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

template = getTemplate('class.swift')

# TODO: figure out how to do this in Jinja instead
example_json['arg_list'] = ", ".join([prop_name+": "+prop_type for prop_name, prop_type in example_json['properties'].items()])


def args_with_cast(properties, json_mapping):
    result_arr = []
    for json_key, prop_name in json_mapping.items():
        arg_with_cast = '{0}: json["{1}"] as {2}'.format(prop_name, json_key, properties[prop_name])
        result_arr.append(arg_with_cast)
    return ", ".join(result_arr)

example_json['init_args_with_casts'] = args_with_cast(example_json["properties"], json_key_to_property)

example_json['json_mapping'] = json_key_to_property

print template.render(example_json)


# just had this crazy idea that could curry the initializer
