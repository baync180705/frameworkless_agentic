TOOLS_SCHEMA = [
    {
        "function_declarations": [
            {
                "name": "read_file",
                "description": "Read the contents of a file",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "path": {
                            "type": "string",
                            "description": "Path to the file"
                        }
                    },
                    "required": ["path"]
                }
            },
            {
            "name": "list_files",
            "description": "List all files and directories at the given path",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Directory path to list files from. Defaults to current directory."
                    }
                },
                "required": []
            }
        }
        ],
        
    }
]
