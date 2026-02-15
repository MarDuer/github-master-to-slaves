from github import GithubException

def apply_branch_protection(repo, branch_name, protection_config, logger):
    try:
        branch = repo.get_branch(branch_name)
        
        kwargs = {}
        
        if "required_status_checks" in protection_config:
            rsc = protection_config["required_status_checks"]
            kwargs["strict"] = rsc.get("strict", False)
            kwargs["contexts"] = rsc.get("contexts", [])
        
        if "required_pull_request_reviews" in protection_config:
            rpr = protection_config["required_pull_request_reviews"]
            kwargs["require_code_owner_reviews"] = rpr.get("require_code_owner_reviews", False)
            kwargs["dismiss_stale_reviews"] = rpr.get("dismiss_stale_reviews", False)
            kwargs["required_approving_review_count"] = rpr.get("required_approving_review_count", 1)
        
        kwargs["enforce_admins"] = protection_config.get("enforce_admins", False)
        
        if "restrictions" in protection_config:
            rest = protection_config["restrictions"]
            kwargs["user_push_restrictions"] = rest.get("users", [])
            kwargs["team_push_restrictions"] = rest.get("teams", [])
        
        branch.edit_protection(**kwargs)
        
        logger.log(
            repo.full_name,
            "branch_protection",
            "apply",
            {"branch": branch_name, "protection": protection_config},
            "success"
        )
        return True
        
    except GithubException as e:
        logger.log(
            repo.full_name,
            "branch_protection",
            "apply",
            {"branch": branch_name},
            "error",
            str(e)
        )
        return False

def remove_branch_protection(repo, branch_name, logger):
    try:
        branch = repo.get_branch(branch_name)
        branch.remove_protection()
        
        logger.log(
            repo.full_name,
            "branch_protection",
            "remove",
            {"branch": branch_name},
            "success"
        )
        return True
        
    except GithubException as e:
        logger.log(
            repo.full_name,
            "branch_protection",
            "remove",
            {"branch": branch_name},
            "error",
            str(e)
        )
        return False
