def compare_branch_protection(master_branches, target_branches):
    master_dict = {b["name"]: b for b in master_branches}
    target_dict = {b["name"]: b for b in target_branches}
    
    changes = {
        "additions": [],
        "modifications": [],
        "deletions": []
    }
    
    for branch_name, master_branch in master_dict.items():
        if branch_name not in target_dict:
            if "protection" in master_branch:
                changes["additions"].append({
                    "branch": branch_name,
                    "protection": master_branch["protection"]
                })
        else:
            target_branch = target_dict[branch_name]
            master_protection = master_branch.get("protection")
            target_protection = target_branch.get("protection")
            
            if master_protection != target_protection:
                changes["modifications"].append({
                    "branch": branch_name,
                    "old": target_protection,
                    "new": master_protection
                })
    
    for branch_name, target_branch in target_dict.items():
        if branch_name not in master_dict and "protection" in target_branch:
            changes["deletions"].append({
                "branch": branch_name,
                "protection": target_branch["protection"]
            })
    
    changes["has_changes"] = bool(changes["additions"] or changes["modifications"] or changes["deletions"])
    return changes
