from registry_reader import RegistryReader
from schema_loader import SchemaLoader
from validator import RegistryValidator

def main():
    schema = SchemaLoader().load("application.schema.json")
    validator = RegistryValidator(schema)
    
    # Load all applications
    applications = {filename: app for filename, app in RegistryReader().load_all()}
    
    failed = False
    project_ids = {}

    for filename, application in applications.items():
        # 1. Schema Validation (assumes schema covers presence/type requirements)
        errors = validator.validate(application)
        
        # 2. Field Existence Validations
        required_fields = [
            "schemaVersion", "product", "team", "owner", 
            "budgetOwner", "organization", "department", 
            "costCenter", "bindings"
        ]
        
        for field in required_fields:
            if field not in application:
                errors.append(f"Missing required field: {field}")

        # 3. Bindings Validation
        if "bindings" in application:
            if not isinstance(application["bindings"], list):
                errors.append("Field 'bindings' must be a list")
            else:
                for binding in application["bindings"]:
                    # Validate individual binding structure
                    required_binding_keys = [
                        "cloud", "projectId", "region", 
                        "environment", "businessCriticality"
                    ]
                    for key in required_binding_keys:
                        if key not in binding:
                            errors.append(f"Binding missing required key: {key}")
                    
                    # Cross-file Project ID Uniqueness
                    if "projectId" in binding:
                        p_id = binding["projectId"]
                        if p_id in project_ids:
                            print(f"Duplicate projectId '{p_id}' found in "
                                  f"{project_ids[p_id]} and {filename}")
                            failed = True
                        project_ids[p_id] = filename

        # Reporting errors
        if errors:
            failed = True
            print(f"\n{filename}")
            for error in errors:
                # Handle error objects vs string messages
                msg = error.message if hasattr(error, 'message') else error
                print(f"  - {msg}")
        else:
            print(f"{filename} ✓")

    if failed:
        raise SystemExit(1)

    print("\nRegistry validation successful")

if __name__ == "__main__":
    main()