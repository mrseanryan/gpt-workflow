import json

import config

def try_add_missing_quotes(rsp):
    # rsp almost valid, but no quotes on the keys!
    #example:
    #     {
    # bot_name: "Document Creator Bot",
    # command_name: "Create Document",
    # message_to_user: "What type of document would you like to create? Text, Image, or Spreadsheet?",
    # document_type: None
    # }
    new_rsp = ""
    split_by_space = rsp.split(" ")
    for x in split_by_space:
        if x.endswith(':'):
            x = f'"{x}":'
        new_rsp += x + " "
    return new_rsp

def force_to_json(rsp, property_name):
    try:
        if config.is_debug:
            print("RSP: ")
            print(rsp)
            print("")
        json.loads(rsp, strict=False)
        return rsp
    except Exception as e1:
        if config.is_debug:
            print(e1)
            print("RSP: ")
            print(rsp)
        try:
            rsp = rsp.replace("Output:", "")
            if config.is_debug:
                print(rsp)
            json.loads(rsp, strict=False)
            return rsp    
        except Exception as e1:
            if config.is_debug:
                print(e1)
                print("RSP: ")
                print(rsp)
            try:
                rsp = try_add_missing_quotes(rsp)
                if config.is_debug:
                    print(rsp)
                json.loads(rsp, strict=False)
                return rsp
            except Exception:
                if not ":" in rsp: # not already an attempt at JSON
                    dict = {
                        property_name: rsp
                    }
                    return json.dumps(dict)
                else: # an attempt at JSON, but not valid JSON!
                    dict = {
                        property_name: "Cannot answer this question",
                        "error": "Invalid JSON",
                        "original": rsp
                    }
                    return json.dumps(dict)
