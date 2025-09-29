<#
PowerShell helper to initialize git, create a repo, add remote and push.
Usage: Run in the project root (where this script lives):
  ./init_and_push.ps1 -RemoteUrl 'https://github.com/username/repo.git' -Branch 'main'
#>
param(
    [Parameter(Mandatory=$true)]
    [string]$RemoteUrl,

    [string]$Branch = 'main'
)

Write-Host "Initializing local git repository..."
if (!(Test-Path -Path .git)) {
    git init
    git add .
    git commit -m "chore: initial commit"
} else {
    Write-Host ".git already exists, skipping git init."
}

Write-Host "Adding remote origin: $RemoteUrl"
try {
    git remote add origin $RemoteUrl -ErrorAction Stop
} catch {
    Write-Host "Remote may already exist; setting url instead."
    git remote set-url origin $RemoteUrl
}

Write-Host "Pushing to remote $Branch (you may be prompted for credentials)..."
# Create branch if not exists
try {
    git branch --list $Branch | Out-Null
    git checkout -B $Branch
} catch {
    git checkout -b $Branch
}

git push -u origin $Branch

Write-Host "Push complete. Please check your GitHub repository."
