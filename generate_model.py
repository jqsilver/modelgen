#!/bin/python
import json
import jinja2
import string


def getTemplate(name):
    return env.get_template(name)

def validateMapping(class_json, json_to_property):
    mapped_properties = json_to_property.values()
    for prop_name in class_json["properties"].keys():
        if prop_name not in mapped_properties:
            print "// missing "+prop_name
            return False
    return True

# formats a (prop_name, prop_type) tuple into an argument.
# takes a tuple for easy calling with map
def formatForArgument(property_tuple):
    (prop_name, prop_type) = property_tuple
    return prop_name+": "+prop_type



#set up templates
loader = jinja2.FileSystemLoader(searchpath="./templates")
env = jinja2.Environment(loader=loader, trim_blocks=True, lstrip_blocks=True)
env.filters['formatForArgument'] = formatForArgument

template = env.get_template('class.swift')
#template = env.get_template('test.txt')

class_spec_json = json.loads(open('./example/ExampleSpec.json', 'r').read())
json_key_to_property = json.loads(open('./example/ExampleMapping.json', 'r').read())

if not validateMapping(class_spec_json, json_key_to_property):
    print "// Missing required properties in mapping"


# TODO: figure out how to do this in Jinja instead
#class_spec_json['arg_list'] = ", ".join([prop_name+": "+prop_type for prop_name, prop_type in class_spec_json['properties'].items()])

def formatForArgumentWithCast(mapping_tuple):
    (json_key, prop_name) = mapping_tuple
    prop_type = class_spec_json["properties"][prop_name]
    return '{0}: json["{1}"] as {2}'.format(prop_name, json_key, prop_type)
env.filters['formatForArgumentWithCast'] = formatForArgumentWithCast

class_spec_json['json_key_to_property'] = json_key_to_property

print template.render(class_spec_json)


# just had this crazy idea that could curry the initializer
