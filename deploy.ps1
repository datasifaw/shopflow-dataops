
# ShopFlow DataOps - SCRUM-23
# Deploiement SQL Server

$ErrorActionPreference = "Stop"

$server = ".\SQLEXPRESS"
$projectRoot = $PSScriptRoot

$scripts = @(
    "sql/01_create_database.sql",
    "sql/02_create_tables.sql",
    "sql/03_constraints_indexes.sql"
)

if (-not (Get-Command sqlcmd -ErrorAction SilentlyContinue)) {
    throw "sqlcmd introuvable."
}

foreach ($script in $scripts) {
    $path = Join-Path $projectRoot $script

    if (-not (Test-Path $path)) {
        throw "Fichier introuvable : $path"
    }
}

foreach ($script in $scripts) {
    $path = Join-Path $projectRoot $script

    Write-Host "Execution : $script"

    & sqlcmd -S $server -E -C -b -i $path

    if ($LASTEXITCODE -ne 0) {
        throw "Echec SQL : $script"
    }

    Write-Host "OK : $script"
}

Write-Host "Deploiement termine avec succes."
