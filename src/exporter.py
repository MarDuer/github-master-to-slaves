import json
from github import GithubException

def export_branch_protection(repo):
    branches_data = []
    
    for branch in repo.get_branches():
        branch_info = {"name": branch.name}
        
        try:
            protection = branch.get_protection()
            branch_info["protection"] = _serialize_protection(protection)
        except GithubException:
            pass
        
        branches_data.append(branch_info)
    
    return branches_data

def _serialize_protection(protection):
    data = {}
    
    if protection.required_status_checks:
        data["required_status_checks"] = {
            "strict": protection.required_status_checks.strict,
            "contexts": protection.required_status_checks.contexts
        }
    
    if protection.required_pull_request_reviews:
        reviews = protection.required_pull_request_reviews
        data["required_pull_request_reviews"] = {
            "dismiss_stale_reviews": reviews.dismiss_stale_reviews,
            "require_code_owner_reviews": reviews.require_code_owner_reviews,
            "required_approving_review_count": reviews.required_approving_review_count
        }
        if reviews.dismissal_users:
            data["required_pull_request_reviews"]["dismissal_users"] = [u.login for u in reviews.dismissal_users]
        if reviews.dismissal_teams:
            data["required_pull_request_reviews"]["dismissal_teams"] = [t.slug for t in reviews.dismissal_teams]
    
    data["enforce_admins"] = protection.enforce_admins.enabled if protection.enforce_admins else False
    
    if protection.restrictions:
        data["restrictions"] = {
            "users": [u.login for u in protection.restrictions.users],
            "teams": [t.slug for t in protection.restrictions.teams]
        }
    
    return data

def save_branch_protection(branches_data, settings_dir):
    output_file = settings_dir / "branch-protection.json"
    with open(output_file, "w") as f:
        json.dump(branches_data, f, indent=2)
    return output_file
