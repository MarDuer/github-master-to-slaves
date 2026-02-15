# Fork + Sync Strategy

## Overview

This repository can serve as both a **content template** and a **settings master** for your projects. By combining GitHub's fork functionality with the settings sync tool, you get the best of both worlds.

## The Strategy

### 1. Fork for Content
Fork this repository to create new projects that inherit:
- Initial code structure
- Documentation templates
- Configuration files
- Workflow files

### 2. Sync for Settings
Use the sync tool to enforce consistent settings across all forks:
- Branch protection rules
- Required status checks
- Review requirements
- Security settings

## Workflow

### Initial Setup

```bash
# 1. Fork this repository to create a new project
gh repo fork MarDuer/github-master-to-slaves \
  --org your-org \
  --fork-name my-new-project

# 2. Add the sync topic to the fork
gh repo edit your-org/my-new-project --add-topic sync-from-master

# 3. Clone the fork and start working
gh repo clone your-org/my-new-project
cd my-new-project
```

### Keeping Content Updated

Pull content updates from the master repository:

```bash
# Add upstream remote (if not already added)
git remote add upstream https://github.com/MarDuer/github-master-to-slaves.git

# Fetch and merge updates from master
git fetch upstream
git merge upstream/main

# Or use rebase for cleaner history
git rebase upstream/main
```

### Keeping Settings Updated

Use the sync tool to apply settings changes:

```bash
# In the master repository
cd github-master-to-slaves

# Export current settings
just export MarDuer/github-master-to-slaves

# Preview changes to all forks
just dry-run

# Apply settings to all forks with the topic
just sync
```

## Benefits

### ✅ Advantages

1. **Content Inheritance** - Forks get all initial content from master
2. **Easy Updates** - Pull content changes from upstream
3. **Consistent Settings** - Sync tool enforces settings across all forks
4. **Flexible** - Can detach fork later if needed
5. **Scalable** - Works for any number of forks
6. **Reversible** - Can always break the fork relationship

### 🎯 Use Cases

**Perfect for:**
- Creating multiple projects from the same template
- Maintaining consistent standards across an organization
- Sharing boilerplate code and configurations
- Enforcing security policies across projects

**Example Scenarios:**
- Microservices architecture (multiple services, same standards)
- Multi-tenant applications (one codebase, multiple deployments)
- Team projects (consistent setup for all team repositories)
- Client projects (same foundation, different customizations)

## Detaching a Fork (Optional)

If you later decide you want a fork to be completely independent:

### Option 1: GitHub Support
1. Go to fork repository Settings
2. Scroll to bottom where it says "This is a fork"
3. Contact GitHub Support to detach the fork

### Option 2: Manual Recreation
```bash
# Clone the fork
git clone https://github.com/your-org/forked-repo.git
cd forked-repo

# Create new independent repository
gh repo create your-org/independent-repo --source=. --remote=origin --push

# Delete the old fork
gh repo delete your-org/forked-repo --yes
```

After detaching, the repository becomes independent but can still use the sync tool for settings.

## Example: Multi-Project Organization

```
Master Repository (github-master-to-slaves)
├── Branch protection: 2 approvals required
├── Required checks: CI, lint, security scan
└── Settings: settings/branch-protection.json

Forked Projects (all with topic "sync-from-master")
├── api-service (fork + custom API code)
├── web-frontend (fork + custom UI code)
├── mobile-app (fork + custom mobile code)
└── admin-dashboard (fork + custom admin code)

All projects:
✅ Share the same branch protection rules
✅ Require the same status checks
✅ Can pull template updates from master
✅ Maintain their own unique code
```

## Workflow Diagram

```
┌─────────────────────────────────────┐
│   Master Repository                 │
│   (github-master-to-slaves)         │
│                                     │
│   - Template code                   │
│   - Settings definitions            │
│   - Documentation                   │
└──────────────┬──────────────────────┘
               │
               │ Fork (content)
               ├──────────────────────┐
               │                      │
               ▼                      ▼
    ┌──────────────────┐   ┌──────────────────┐
    │  Fork 1          │   │  Fork 2          │
    │  + topic tag     │   │  + topic tag     │
    └──────────────────┘   └──────────────────┘
               │                      │
               │                      │
               └──────────┬───────────┘
                          │
                          │ Sync (settings)
                          ▼
                   ┌──────────────┐
                   │  Sync Tool   │
                   │  (just sync) │
                   └──────────────┘
```

## Configuration

### Master Repository Setup

1. **Configure settings** in `settings/branch-protection.json`
2. **Set target topic** in `config.json`:
   ```json
   {
     "target_topic": "sync-from-master",
     "stop_on_error": false
   }
   ```

### Fork Repository Setup

1. **Add topic** `sync-from-master` to the fork
2. **Ensure admin access** for the GitHub token
3. **No additional configuration needed** - settings come from master

## Best Practices

### 1. Version Control Settings
- Commit settings changes to master repository
- Review settings changes via Pull Requests
- Use semantic versioning for major settings changes

### 2. Test Before Applying
- Always run `just dry-run` before `just sync`
- Test settings on a single fork first
- Monitor logs for errors

### 3. Document Customizations
- If a fork needs different settings, document why
- Consider if the exception should become the rule
- Use repo-specific settings files if needed

### 4. Regular Syncs
- Schedule regular settings syncs (weekly/monthly)
- Sync after any security policy changes
- Sync when onboarding new team members

### 5. Communication
- Notify teams before major settings changes
- Document breaking changes in commit messages
- Provide migration guides for significant updates

## Troubleshooting

### Fork doesn't receive settings updates
- Verify the fork has the `sync-from-master` topic
- Check that your GitHub token has admin access to the fork
- Run `just discover` to see if the fork is detected

### Content conflicts when pulling from upstream
```bash
# Resolve conflicts manually
git fetch upstream
git merge upstream/main
# Fix conflicts in your editor
git add .
git commit
```

### Want to stop syncing a specific fork
- Remove the `sync-from-master` topic from the fork
- The fork will no longer receive settings updates
- Content relationship remains intact

## Conclusion

The fork + sync strategy provides a powerful way to maintain both content templates and consistent settings across multiple repositories. It's flexible, scalable, and reversible - perfect for organizations managing multiple related projects.

Start by forking this repository, add the sync topic, and let the tool handle the rest!
