import json

def validate_branch_protection_schema(data):
    if not isinstance(data, list):
        raise ValueError("Branch protection settings must be a list")
    
    for branch in data:
        if not isinstance(branch, dict):
            raise ValueError("Each branch must be a dictionary")
        
        if "name" not in branch:
            raise ValueError("Branch must have a 'name' field")
        
        if "protection" in branch:
            protection = branch["protection"]
            if not isinstance(protection, dict):
                raise ValueError(f"Protection for branch '{branch['name']}' must be a dictionary")
            
            if "required_status_checks" in protection:
                rsc = protection["required_status_checks"]
                if "strict" not in rsc or "contexts" not in rsc:
                    raise ValueError(f"Invalid required_status_checks for branch '{branch['name']}'")
            
            if "required_pull_request_reviews" in protection:
                rpr = protection["required_pull_request_reviews"]
                if "required_approving_review_count" in rpr:
                    count = rpr["required_approving_review_count"]
                    if not isinstance(count, int) or count < 1 or count > 6:
                        raise ValueError(f"Invalid required_approving_review_count for branch '{branch['name']}': must be 1-6")
    
    return True

def validate_settings_file(file_path):
    try:
        with open(file_path) as f:
            data = json.load(f)
        validate_branch_protection_schema(data)
        return True, None
    except json.JSONDecodeError as e:
        return False, f"Invalid JSON: {e}"
    except ValueError as e:
        return False, str(e)
    except Exception as e:
        return False, f"Validation error: {e}"
