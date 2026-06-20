param(
    [Parameter(Mandatory=$true)][string]$InputFile,
    [Parameter(Mandatory=$true)][string]$OutputFile,
    [Parameter(Mandatory=$false)][string]$Format = "png"
)
$ErrorActionPreference = "Stop"

$drawioCmd = $null
$paths = @(
    "C:\Program Files\draw.io\draw.io.exe",
    "C:\Program Files (x86)\draw.io\draw.io.exe",
    "${env:LOCALAPPDATA}\Programs\draw.io\draw.io.exe",
    "${env:USERPROFILE}\AppData\Local\Programs\draw.io\draw.io.exe"
)

foreach ($p in $paths) {
    if (Test-Path $p) {
        $drawioCmd = $p
        break
    }
}

if (-not $drawioCmd) {
    $found = Get-Command "draw.io" -ErrorAction SilentlyContinue
    if ($found) {
        $drawioCmd = $found.Source
    }
}

if (-not $drawioCmd) {
    Write-Error "draw.io desktop not found. Download from https://github.com/jgraph/drawio-desktop/releases"
    exit 1
}

$argsList = @("--export", "--format", $Format, "--output", $OutputFile)

if ($Format -eq "png") {
    $argsList += @("--scale", "2", "--border", "20")
}

$argsList += $InputFile

& $drawioCmd @argsList

if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
}
